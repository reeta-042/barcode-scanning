import os
from google import genai
from google.genai import types
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def call_llm_model(metadata: dict, language:str):
    product_name = metadata.get("product_name", "")
    brand = metadata.get("brand", "")
    category = metadata.get("category", "")
    use = metadata.get("use", "")
    pack_size = metadata.get("pack_size", "")
    features = metadata.get("features", "")

    prompt = (
    f"- Respond with the selected language: {language}\n"
    f"- Let your response also be in a html format\n"
    f"Based on the following metadata, the product has been validated and confirmed as authentic.\n"
    f"Now speak to the user calmly and reassuringly, as if you’ve reviewed the product yourself.\n"
    f"Tell the user what you think about the product and what you feel they should know.\n"
    f"Your total response should be  exactly  300 characters.\n"
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

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0) # Disables thinking
        ),
    )

    # It's good practice to return responses
    if response and hasattr(response, 'text'):
        return response.text
    else:
        return "⚠️ No valid response received from AI ASSISTANT."
