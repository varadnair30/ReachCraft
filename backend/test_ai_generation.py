import httpx
import json

print("🧪 Testing AI Generation API...\n")

base_url = "http://127.0.0.1:8000"

# Test 1: Generate subject lines
print("Test 1: Generate Subject Lines")
subject_data = {
    "recipient_first_name": "Sarah",
    "recipient_company": "Google",
    "recipient_title": "Engineering Manager",
    "sender_name": "Varad Nair",
    "sender_current_role": "Full-Stack Engineer",
    "purpose": "job_inquiry"
}

try:
    response = httpx.post(
        f"{base_url}/api/ai-generation/generate-subject",
        json=subject_data,
        timeout=60.0
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Request failed: {e}")

print()

# Test 2: Generate complete email
print("Test 2: Generate Complete Email")
complete_data = {
    "recipient_first_name": "Sarah",
    "recipient_last_name": "Johnson",
    "recipient_company": "Google",
    "recipient_title": "Engineering Manager",
    "sender_name": "Varad Nair",
    "sender_email": "varad@example.com",
    "sender_background": "4+ years full-stack development at Fortune 500 companies",
    "sender_skills": ["React", "Python", "FastAPI", "PostgreSQL", "Docker", "GCP"],
    "sender_portfolio": "https://varadnair30.github.io/my_portfolio/",
    "sender_linkedin": "https://linkedin.com/in/varad-nair",
    "purpose": "job_inquiry",
    "role_interested_in": "Senior Full-Stack Engineer",
    "tone": "professional"
}

try:
    response = httpx.post(
        f"{base_url}/api/ai-generation/generate-complete",
        json=complete_data,
        timeout=60.0
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Subject: {result['subject_line']}")
        print(f"Confidence: {result['confidence_score']}")
        print("\nSubject Variations:")
        for i, subj in enumerate(result["subject_variations"], 1):
            print(f"  {i}. {subj}")
        print(f"\nBody:\n{result['body']}")
        print(f"\nWord Count: {result['word_count']}")
        print(f"Read Time: {result['estimated_read_time']} seconds")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Request failed: {e}")
