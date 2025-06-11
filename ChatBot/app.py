import os
from google import genai
from dotenv import load_dotenv
load_dotenv()

def main():
    client = genai.Client(api_key= os.getenv("GEMINI_API_KEY"))
    chat = client.chats.create(model="gemini-2.0-flash")
    while(True):
        message = input("User: ")
        if message == "bye":
            break 
        
        response = chat.send_message_stream(message)
        for chunk in response:
            print(chunk.text, end="")
main()