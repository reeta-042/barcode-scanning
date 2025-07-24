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
    f"Based on the following metadata, assume the product has been validated and confirmed as authentic.\n"
    f"Now speak to the user calmly and reassuringly, as if you’ve reviewed the product yourself.\n"
    f"Tell the user what you think about the product and what you feel they should know.\n"
    f"In no more than 300 characters, summarize what the user should know:\n"
    f"Be gentle in tone, informative, and user-friendly.\n\n"
    f"Metadata:\n"
    f"- Product Name: {product_name}\n"
    f"- Brand: {brand}\n"
    f"- Category: {category}\n"
    f"- Use: {use}\n"
    f"- Pack Size: {pack_size}\n"
    f"- Features: {features}\n\n"
    f"Include in your response:\n"
    f"- A very brief product summary\n"
    f"- One gentle key benefit of the product\n"
    f"- Two bullet-point safety precautions\n"
    f"- Relevant Packaging details\n"
    f"- Two frequently asked questions with answers\n"
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
