
import os
from dotenv import load_dotenv

load_dotenv()

print("🔍 Testing API Keys...\n")

# Test Supabase
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
print(f"✅ Supabase URL: {supabase_url[:30]}...")
print(f"✅ Supabase Key: {supabase_key[:30]}...\n")

# Test Gemini
gemini_key = os.getenv("GOOGLE_API_KEY")
print(f"✅ Gemini API Key: {gemini_key[:20]}...\n")

# Test Resend
resend_key = os.getenv("RESEND_API_KEY")
print(f"✅ Resend API Key: {resend_key[:20]}...\n")

print("🎉 All API keys loaded successfully!")
