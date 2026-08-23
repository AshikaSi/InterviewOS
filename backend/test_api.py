import google.genai as genai
from config import settings

print(f"API Key: {settings.GEMINI_API_KEY[:30]}...")

try:
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents="Say hello"
    )
    print(f"✅ Success: {response.text}")
except Exception as e:
    print(f"❌ Error: {e}")