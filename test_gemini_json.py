import google.generativeai as genai
import json

import os

api_key = os.environ.get("GEMINI_API_KEY", "")
if api_key:
    genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")
resp = model.generate_content(
    "Extrae: nombre y edad de 'Juan tiene 30 años'",
    generation_config=genai.GenerationConfig(response_mime_type="application/json")
)
print(resp.text)
