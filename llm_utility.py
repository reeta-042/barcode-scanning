from openai import OpenAI
import os

# 🔌 Connect to OpenRouter
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

def call_llm_model(metadata: dict):
    product_name = metadata.get("product_name", "")
    brand = metadata.get("brand", "")
    category = metadata.get("category", "")
    use = metadata.get("use", "")
    pack_size = metadata.get("pack_size", "")
    features = metadata.get("features", "")

    prompt = (
        f"Based on the following metadata:\n"
        f"Product Name: {product_name}\n"
        f"Brand: {brand}\n"
        f"Category: {category}\n"
        f"Use: {use}\n"
        f"Pack Size: {pack_size}\n"
        f"Features: {features}\n\n"
        f"Generate the following:\n"
        f"- A very brief product summary\n"
        f"- One very brief Key product benefits\n"
        f"- 2 bullet points Safety precautions\n"
        f"- Packaging details\n"
        f"- Two short frequently asked questions with answers"
    )

    response = client.chat.completions.create(
        model="meta-llama/llama-3.3-70b-instruct:free",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=500
    )

    if response and response.choices and response.choices[0].message:
        return response.choices[0].message.content
    else:
        return None
