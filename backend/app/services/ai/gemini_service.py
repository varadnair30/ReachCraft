import os
import json
import google.generativeai as genai
from typing import List, Tuple, Dict, Any
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

class GeminiService:
    '''Service for interacting with Google Gemini Flash'''
    
    def __init__(self, model_name: str = 'gemini-2.5-flash'):
        self.model = genai.GenerativeModel(model_name)
        
        # Generation config for better control
        self.generation_config = {
            'temperature': 0.7,
            'top_p': 0.9,
            'top_k': 40,
            'max_output_tokens': 4096,
        }
        
        # Safety settings (relaxed for professional use)
        self.safety_settings = [
            {
                'category': 'HARM_CATEGORY_HARASSMENT',
                'threshold': 'BLOCK_NONE'
            },
            {
                'category': 'HARM_CATEGORY_HATE_SPEECH',
                'threshold': 'BLOCK_NONE'
            },
            {
                'category': 'HARM_CATEGORY_SEXUALLY_EXPLICIT',
                'threshold': 'BLOCK_NONE'
            },
            {
                'category': 'HARM_CATEGORY_DANGEROUS_CONTENT',
                'threshold': 'BLOCK_NONE'
            },
        ]
    
    def generate(self, prompt: str) -> str:
        '''Generate text from prompt'''
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config,
                safety_settings=self.safety_settings
            )
            return response.text
        except Exception as e:
            raise Exception(f'Gemini generation error: {str(e)}')
    
    def generate_json(self, prompt: str) -> Dict[str, Any]:
        '''Generate JSON response from prompt'''
        response_text = None
        try:
            response_text = self.generate(prompt)
            
            # Try to parse JSON from response
            # Sometimes Gemini adds markdown code blocks
            if '```json' in response_text:
                # Extract JSON from markdown
                parts = response_text.split('```json')
                if len(parts) > 1:
                    json_str = parts[1].split('```')[0].strip()
                else:
                    json_str = response_text.strip()
            elif '```' in response_text:
                parts = response_text.split('```')
                if len(parts) > 1:
                    json_str = parts[1].strip()
                else:
                    json_str = response_text.strip()
            else:
                json_str = response_text.strip()
            
            return json.loads(json_str)
        
        except json.JSONDecodeError as e:
            raise Exception(f'Failed to parse JSON from Gemini: {str(e)}. Response: {response_text}')
        except Exception as e:
            raise Exception(f'Gemini JSON generation error: {str(e)}')

    
    def generate_subject_lines(self, prompt: str) -> List[str]:
        '''Generate multiple subject line variations'''
        response_text = None
        try:
            response_text = self.generate(prompt)
            
            # Try to parse as JSON array
            if '```json' in response_text:
                parts = response_text.split('```json')
                if len(parts) > 1:
                    json_str = parts[1].split('```')[0].strip()
                else:
                    json_str = response_text.strip()
            elif '```' in response_text:
                parts = response_text.split('```')
                if len(parts) > 1:
                    json_str = parts[1].strip()
                else:
                    json_str = response_text.strip()
            elif '[' in response_text and ']' in response_text:
                # Extract array
                start = response_text.index('[')
                end = response_text.rindex(']') + 1
                json_str = response_text[start:end]
            else:
                json_str = response_text.strip()
            
            subject_lines = json.loads(json_str)
            
            if not isinstance(subject_lines, list):
                raise ValueError('Expected list of subject lines')
            
            return subject_lines
        
        except Exception as e:
            # Fallback: split by newlines if we have response_text
            if response_text:
                lines = response_text.strip().split('\n')
                cleaned = []
                for line in lines:
                    line = line.strip()
                    line = line.lstrip('0123456789.-* ')
                    line = line.strip('"\'')
                    if line and len(line) > 10:
                        cleaned.append(line)
                
                return cleaned[:3] if cleaned else ['Following up on our conversation']
            else:
                return ['Following up on our conversation', 'Question about your team', 'Brief introduction']
    
    def calculate_confidence(self, email_body: str) -> float:
        '''
        Calculate confidence score based on email quality
        Checks for cliches, length, structure
        '''
        score = 1.0
        
        # Cliche detection (reduce score)
        cliches = [
            'passionate', 'rockstar', 'ninja', 'guru',
            'fast-paced environment', 'team player',
            'think outside the box', 'hit the ground running',
            'hope this email finds you well',
            'would love the opportunity'
        ]
        
        lower_body = email_body.lower()
        for cliche in cliches:
            if cliche in lower_body:
                score -= 0.1
        
        # Length check
        word_count = len(email_body.split())
        if word_count > 200:
            score -= 0.2
        elif word_count < 50:
            score -= 0.3
        
        # Structure check (paragraphs)
        paragraphs = [p for p in email_body.split('\n\n') if p.strip()]
        if len(paragraphs) < 2:
            score -= 0.1
        
        return max(0.0, min(1.0, score))
