import google.generativeai as genai
import os
from dotenv import load_dotenv
import time

load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

print('Testing Gemini 2.5 Flash directly...\n')

model = genai.GenerativeModel('gemini-2.5-flash')

start = time.time()
try:
    response = model.generate_content('Say hello in one sentence.')
    print(f'✅ Success! ({time.time() - start:.2f}s)')
    print(f'Response: {response.text}')
except Exception as e:
    print(f'❌ Error: {e}')
