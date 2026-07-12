from openai import OpenAI

from config import load_config

config = load_config()

client = OpenAI(
    api_key=config.ai.nvidia_api_key,
    base_url="https://integrate.api.nvidia.com/v1",
)

response = client.chat.completions.create(
    model=config.ai.nvidia_model,
    messages=[
        {
            "role": "user",
            "content": "Reply with exactly: Hello",
        }
    ],
)

print(response.choices[0].message.content)