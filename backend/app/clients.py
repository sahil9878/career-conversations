from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
class OpenAIClient:
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)
    context = ""

    with open("app/context.txt", "r") as file:
        context = file.read()
    
    system_prompt  = f"You are acting as Sahil Singh. You are answering questions on Sahil Singh's website, \
                    particularly questions related to Sahil Singh's career, background, skills and experience. \
                    Your responsibility is to represent Sahil Singh for interactions on the website as faithfully as possible. \
                    You are given a summary of Sahil Singh's background which you can use to answer questions. \
                    Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
                    If you don't know the answer, say so.\
                    If you are asked any question that is not related to Sahil Singh's career, background, skills or experience, \
                    politely decline to answer and try to steer the conversation towards Sahil Singh's career, background, skills and experience. \
                    Decline any code requests, and other general queries even if they are simple. "
    
    # If you don't know the answer to any question, use your record_unknown_question tool to record the question that you couldn't answer, even if it's about something trivial or unrelated to career. \
    # If the user is engaging in discussion, try to steer them towards getting in touch via email; ask for their email and record it using your record_user_details tool. "

    system_prompt += f"\n\n## Summary:\n{context}\n\n##"
    system_prompt += f"With this context, please chat with the user, always staying in character as Sahil Singh."

    @staticmethod
    async def send_message(message: str):
        stream =  OpenAIClient.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=
                [{"role": "system", "content": OpenAIClient.system_prompt},
                {"role": "user", "content": message}
            ],
            stream=True
        )
        response = ""
        for chunk in stream:
            curr = chunk.choices[0].delta.content
            response += curr or ""
            print(curr or "", end="")

        return response