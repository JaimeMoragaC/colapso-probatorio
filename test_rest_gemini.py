import urllib.request
import urllib.parse
import os

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

schema = {
    "type": "object",
    "properties": {
        "nombre": {"type": "string"},
        "edad": {"type": "integer"}
    },
    "required": ["nombre", "edad"]
}

payload = {
    "contents": [{"parts": [{"text": "Juan tiene 30 años"}]}],
    "generationConfig": {
        "responseMimeType": "application/json",
        "responseSchema": schema
    }
}
data = json.dumps(payload).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
try:
    with urllib.request.urlopen(req) as response:
        res = json.loads(response.read().decode('utf-8'))
        print(res['candidates'][0]['content']['parts'][0]['text'])
except Exception as e:
    print(e)
    if hasattr(e, 'read'):
        print(e.read().decode())
