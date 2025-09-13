from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionMessageParam
import os
from dotenv import load_dotenv
from app.clients.mongoClient import mongo
from typing import List, TypedDict


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
                        If you don't know the answer, say so. Do not share any personal information\
                        If you are asked any question that is not related to Sahil Singh's career, background, skills or experience, \
                        politely decline to answer and try to steer the conversation towards Sahil Singh's career, background, skills and experience. \
                        Decline any code requests, and other general queries even if they are simple. "
        
        # If you don't know the answer to any question, use your record_unknown_question tool to record the question that you couldn't answer, even if it's about something trivial or unrelated to career. \
        # If the user is engaging in discussion, try to steer them towards getting in touch via email; ask for their email and record it using your record_user_details tool. "

        self.system_prompt += f"\n\n## Summary:\n{self.context}\n\n##"
        self.system_prompt += f"With this context, please chat with the user, always staying in character as Sahil Singh."

    async def send_message(self, messages: List[ChatCompletionMessageParam] = []) -> str|None:
        opts = {
            "temperature":  0,
            "top_p":  0.9,
            "top_k":  40,
            "max_tokens":  20000,
        }

        stream = await self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=
                [{"role": "system", "content": self.system_prompt},
                *messages
            ],
            # *opts
            # stream=True
        )
        # response = ""
        # for chunk in stream:
        #     curr = chunk.choices[0].delta.content
        #     response += curr or ""
        #     print(curr or "", end="")

        # return response
        return stream.choices[0].message.content
    

openAIClient = OpenAIClient()