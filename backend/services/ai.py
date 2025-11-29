from openai import OpenAI
import os
import json

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def analyze_recipe(video_metadata: dict):
    prompt = f"""
    Analyze the following cooking video metadata and description to extract recipe details.
    
    Title: {video_metadata['title']}
    Description: {video_metadata['description']}
    
    Please output a JSON object with the following structure:
    {{
        "ingredients": [
            {{"name": "Ingredient Name", "amount": "Amount", "unit": "Unit"}}
        ],
        "summary": [
            "Step 1 summary",
            "Step 2 summary"
        ],
        "steps": [
            {{"timestamp": 10, "description": "Detailed step description"}}
        ]
    }}
    
    For timestamps, estimate based on the description if available, otherwise leave as null or 0.
    """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful cooking assistant."},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"}
    )
    
    return json.loads(response.choices[0].message.content)
