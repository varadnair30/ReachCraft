from typing import Optional, List

class PromptBuilder:
    """Build prompts for AI email generation"""
    
    @staticmethod
    def build_subject_line_prompt(
        recipient_name: str,
        recipient_company: str,
        recipient_title: Optional[str] = None,
        sender_name: str = "",
        sender_role: Optional[str] = None,
        purpose: str = "job_inquiry"
    ) -> str:
        """Build prompt for subject line generation"""
        
        context = f"Recipient: {recipient_name}"
        if recipient_title:
            context += f", {recipient_title}"
        context += f" at {recipient_company}"
        
        if sender_name:
            context += f"\nSender: {sender_name}"
        if sender_role:
            context += f", {sender_role}"
        
        purpose_map = {
            "job_inquiry": "reaching out about job opportunities",
            "networking": "networking and building professional connections",
            "collaboration": "exploring collaboration opportunities",
            "introduction": "introducing myself and my work"
        }
        
        purpose_text = purpose_map.get(purpose, purpose)
        
        prompt = f"""Generate 3 professional, engaging email subject lines for cold outreach.

Context:
{context}

Purpose: {purpose_text}

Requirements:
- Keep it under 60 characters
- Be specific and personalized
- Avoid generic phrases like "Following up" or "Quick question"
- Don't use emojis or excessive punctuation
- Make it compelling but professional
- Reference the company or role when relevant

Return ONLY a JSON array of 3 subject lines, nothing else.
Example format: ["Subject 1", "Subject 2", "Subject 3"]
"""
        
        return prompt
    
    @staticmethod
    def build_complete_email_prompt(
        recipient_first_name: str,
        recipient_company: str,
        sender_name: str,
        recipient_last_name: Optional[str] = None,
        recipient_title: Optional[str] = None,
        sender_email: Optional[str] = None,
        sender_background: Optional[str] = None,
        sender_skills: Optional[List[str]] = None,
        sender_portfolio: Optional[str] = None,
        sender_linkedin: Optional[str] = None,
        purpose: str = "job_inquiry",
        role_interested_in: Optional[str] = None,
        tone: str = "professional"
    ) -> str:
        """Build prompt for complete email generation"""
        
        # Build recipient context
        recipient_context = f"{recipient_first_name}"
        if recipient_last_name:
            recipient_context += f" {recipient_last_name}"
        if recipient_title:
            recipient_context += f", {recipient_title}"
        recipient_context += f" at {recipient_company}"
        
        # Build sender context
        sender_context = f"Sender: {sender_name}"
        if sender_background:
            sender_context += f"\nBackground: {sender_background}"
        if sender_skills and len(sender_skills) > 0:
            sender_context += f"\nSkills: {', '.join(sender_skills[:5])}"
        
        # Links
        links = []
        if sender_portfolio:
            links.append(f"Portfolio: {sender_portfolio}")
        if sender_linkedin:
            links.append(f"LinkedIn: {sender_linkedin}")
        
        if links:
            sender_context += "\n" + "\n".join(links)
        
        # Purpose mapping
        purpose_map = {
            "job_inquiry": f"exploring {'the ' + role_interested_in + ' role' if role_interested_in else 'opportunities'} at {recipient_company}",
            "networking": f"connecting and learning about work at {recipient_company}",
            "collaboration": f"discussing potential collaboration with {recipient_company}",
            "introduction": f"introducing myself and my background"
        }
        
        purpose_text = purpose_map.get(purpose, purpose)
        
        # Tone guidance
        tone_map = {
            "professional": "Professional and respectful",
            "casual": "Friendly and conversational",
            "enthusiastic": "Energetic and passionate",
            "direct": "Concise and to-the-point"
        }
        
        tone_guidance = tone_map.get(tone, "Professional")
        
        prompt = f"""Generate a professional cold outreach email.

RECIPIENT:
{recipient_context}

SENDER:
{sender_context}

PURPOSE: {purpose_text}
TONE: {tone_guidance}

REQUIREMENTS:
- Keep it under 150 words (ideally 100-120 words)
- Use 2-3 short paragraphs
- Start with a personalized opener (avoid "I hope this email finds you well")
- Mention 1-2 specific, relevant accomplishments
- Include a clear but soft call-to-action
- Don't oversell or use cliches
- Be genuine and human
- End with a simple sign-off

OUTPUT FORMAT (JSON):
{{
  "subject": "Email subject line (under 60 chars)",
  "body": "Complete email body including greeting and sign-off"
}}

Return ONLY valid JSON, no markdown formatting or extra text.
"""
        
        return prompt
