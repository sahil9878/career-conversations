from openai import OpenAI
from openai.types.chat import ChatCompletionMessage, ChatCompletionFunctionToolParam, \
    ChatCompletionMessageFunctionToolCall, ChatCompletionMessageParam, ParsedFunction
from openai.types.chat.chat_completion_message_function_tool_call import Function as ToolFunction
from openai.types.shared_params import FunctionDefinition
import os
from dotenv import load_dotenv
from app.clients.mongoClient import mongo
from typing import List, Union, Sequence
import json
import asyncio


load_dotenv()
class OpenAIClient:
    async def warmup(self):
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)

        self.context = await mongo.get_context()
        
        self.system_prompt  = f"You are acting as Sahil Singh. You are answering questions on Sahil Singh's website, \
                        particularly questions related to Sahil Singh's career, background, skills and experience. \
                        Your responsibility is to represent Sahil Singh for interactions on the website as faithfully as possible. \
                        You are given a summary of Sahil Singh's background which you can use to answer questions. \
                        Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
                        If you don't know the answer, say so and use your record_unknown_question tool to record the question that you couldn't answer, even if it's about something trivial or unrelated to career.\
                        If you are asked any question that is not related to Sahil Singh's career, background, skills or experience, \
                        politely decline to answer and try to steer the conversation towards Sahil Singh's career, background, skills and experience. \
                        Decline any code requests, and other general queries even if they are simple. \
                        If the user is engaging in discussion, try to steer them towards getting in touch via email/phone; ask for their email/phone and record it using your record_user_details tool. \
                        If the user provides their phone number, record it using your record_user_details tool and let them know that you will be in touch soon"
        
        self.system_prompt += f"\n\n## Summary:\n{self.context}\n\n##"
        self.system_prompt += f"With this context, please chat with the user, always staying in character as Sahil Singh."

        record_unknown_question_json: FunctionDefinition = {
            "name": "record_unknown_question",
            "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "The question that couldn't be answered"
                    },
                },
                "required": ["question"],
                "additionalProperties": False
            }
        }
        record_user_details_json: FunctionDefinition = {
            "name": "record_user_details",
            "description": "Use this tool to record that a user is interested in being in touch and provided an email address or phone number",
            "parameters": {
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "description": "The email address of this user"
                    },
                    "name": {
                        "type": "string",
                        "description": "The user's name, if they provided it"
                    },
                    "phone": {
                        "type": "string",
                        "description": "The user's phone number, if they provided it."
                    },
                    "notes": {
                        "type": "string",
                        "description": "Any additional information about the conversation that's worth recording to give context"
                    }
                },
                "required": ["email"],
                "additionalProperties": False
            }
        }
        self.tools: List[ChatCompletionFunctionToolParam] = [{"type": "function", "function": record_user_details_json}, {"type": "function", "function": record_unknown_question_json}]

    async def handle_tool_calls(self, tool_calls):
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            tool = getattr(self, tool_name, None)
            result = await tool(**arguments) if tool else {}
            results.append({"role": "tool","content": json.dumps(result),"tool_call_id": tool_call.id})
        return results

    async def send_message(self, messages: List[ChatCompletionMessageParam] = []):

        async def accumulate_tool_calls(stream):
            nonlocal done

            
            tool_call = ChatCompletionMessageFunctionToolCall(id="0", function=ToolFunction(name="", arguments=""), type="function")
            for chunk in stream:
                choice = chunk.choices[0]
                delta = choice.delta

                # If normal text -> yield or stream
                if delta.content:
                    yield delta

                # If tool call chunk
                if delta.tool_calls:
                    for call_delta in delta.tool_calls:
                        call_id = call_delta.id
                        if call_id:
                            tool_call.id = call_id
                        if call_delta.function.name:
                            tool_call.function.name = call_delta.function.name
                        if call_delta.function.arguments:
                            tool_call.function.arguments += call_delta.function.arguments

                # Check finish reason
                if choice.finish_reason == "tool_calls":
                    # Once finished, yield the fully assembled calls
                    yield ChatCompletionMessage(role="assistant", content="", tool_calls=[tool_call])
                    break
                elif choice.finish_reason == "stop":
                    done = True
                    break



        # opts = {
        #     "temperature":  0,
        #     "top_p":  0.9,
        #     "top_k":  40,
        #     "max_tokens":  4000,
        # }
        # Used to prevent adding tool calls object to the history
        localMessages:Sequence[Union[ChatCompletionMessageParam, ChatCompletionMessage]]  = messages.copy()
        done = False
        while not done:
            stream = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                stream=True,
                messages=
                    [{"role": "system", "content": self.system_prompt},
                    *localMessages,
                    
                ],tools=self.tools)
            
            async for item in accumulate_tool_calls(stream):
                if item.content:
                    yield item.content  # to SSE
                    await asyncio.sleep(0.01)
                elif item.tool_calls:
                    localMessages.append(item)
                    results = await self.handle_tool_calls(item.tool_calls)
                    localMessages.extend(results)


            # for chunk in stream:
            #     delta = chunk.choices[0].delta
            #     if delta.content:
            #         yield delta.content
            #         await asyncio.sleep(0.01)
            #     if chunk.choices[0].finish_reason=="tool_calls" or delta.tool_calls:
            #         tool_calls = delta.tool_calls
            #         if not tool_calls:
            #             continue
            #         results = await self.handle_tool_calls(tool_calls)
            #         localMessages.append(delta) # type: ignore
            #         localMessages.extend(results)

        # for chunk in stream:
        #     if chunk.choices[0].delta.content:
        #         buffer+=chunk.choices[0].delta.content

        #     now = time()
        #     if now - last_flush > 0.2 and buffer:
        #         yield f"id:{counter}\nevent:chatCompletion\ndata:{json.dumps(buffer)}\n\n"
        #         last_flush = now
        #         print(buffer, end="")
        #         counter += 1
        #         buffer=""
        #         await asyncio.sleep(0.005)
        # if buffer:
        #     yield f"id:{counter}\nevent:chatCompletion\ndata:{json.dumps(buffer)}\n\n"


        
    
    async def record_user_details(self, email="email not provided", name="Name not provided", notes="not provided", phone="not provided"):
        await mongo.log_leads(email=email, name=name, notes=notes, phone=phone)
        return {"recorded": "ok"}
    
    async def record_unknown_question(self, question):
        await mongo.log_unknown_question(question)
        return {"recorded": "ok"}
    

openAIClient = OpenAIClient()