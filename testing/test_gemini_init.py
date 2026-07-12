from config import load_config
from ai.gemini import GeminiProvider

config = load_config()

provider = GeminiProvider(config.ai)

response, elapsed = provider._generate_response(
    """
    Return ONLY this JSON:

    {
        "message":"Hello how are you"
    }
    """
)

print(response)
print(elapsed)
# from google import genai
# import os
# from dotenv import load_dotenv

# load_dotenv()

# client = genai.Client(
#     api_key=os.getenv("GEMINI_API_KEY")
# )

# print("Available models:\n")

# for model in client.models.list():
#     print(model.name)