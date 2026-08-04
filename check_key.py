from dotenv import load_dotenv
import os

load_dotenv()

key = os.getenv("GOOGLE_API_KEY")

if key:
    print("API Key Found:")
    print(key)
else:
    print("No API Key Found!")