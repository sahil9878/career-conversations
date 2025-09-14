from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionMessageParam, ChatCompletionFunctionToolParam, ChatCompletionAssistantMessageParam
from openai.types.shared_params import FunctionDefinition
import os
from dotenv import load_dotenv
from app.clients.mongoClient import mongo
from typing import List
import json


load_dotenv()
class OpenAIClient:
    async def warmup(self):
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = AsyncOpenAI(api_key=api_key)

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

    async def send_message(self, messages: List[ChatCompletionMessageParam] = []) -> str|None:
        # opts = {
        #     "temperature":  0,
        #     "top_p":  0.9,
        #     "top_k":  40,
        #     "max_tokens":  4000,
        # }
        # Used to prevent adding tool calls object to the history
        localMessages = messages.copy()
        done = False
        while not done:
            response = await self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=
                [{"role": "system", "content": self.system_prompt},
                *localMessages,
                
            ],tools=self.tools)

            finish_reason = response.choices[0].finish_reason
            
            
            if finish_reason=="tool_calls":
                message = response.choices[0].message
                tool_calls = message.tool_calls
                results = await self.handle_tool_calls(tool_calls)
                localMessages.append(message) # type: ignore
                localMessages.extend(results)
            else:
                done = True

        return response.choices[0].message.content
        # stream = await self.client.chat.completions.create(
        #     model="gpt-4.1-mini",
        #     messages=
        #         [{"role": "system", "content": self.system_prompt},
        #         *messages
        #     ],
        #     # *opts
        #     # stream=True
        # )
        # response = ""
        # for chunk in stream:
        #     curr = chunk.choices[0].delta.content
        #     response += curr or ""
        #     print(curr or "", end="")

        # return response
        
    
    async def record_user_details(self, email="email not provided", name="Name not provided", notes="not provided", phone="not provided"):
        await mongo.log_leads(email=email, name=name, notes=notes, phone=phone)
        return {"recorded": "ok"}
    
    async def record_unknown_question(self, question):
        await mongo.log_unknown_question(question)
        return {"recorded": "ok"}
    

openAIClient = OpenAIClient()