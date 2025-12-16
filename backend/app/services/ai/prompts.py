
from typing import List

SUBJECT_LINE_PROMPT = '''You are an expert at writing compelling, non-cliche email subject lines for job seekers reaching out to recruiters and hiring managers.

CONTEXT:
- Recipient: {recipient_first_name} - {recipient_title} at {recipient_company}
- Sender: {sender_name} - {sender_role}
- Purpose: {purpose}
{context}

RULES:
1. Keep it under 50 characters
2. NO generic phrases like \"Opportunity\", \"Reaching Out\", \"Quick Question\"
3. Make it specific and intriguing
4. Use recipient's name OR company name (not both)
5. Avoid clickbait or spam triggers
6. Be professional but human

GOOD EXAMPLES:
- \"Built a tool {recipient_company} might need\"
- \"{recipient_first_name}, question about your ML stack\"
- \"Similar background to your team at {recipient_company}\"
- \"Loved your post on distributed systems\"

BAD EXAMPLES:
- \"Opportunity at {recipient_company}\" (too generic)
- \"Quick question\" (vague)
- \"Recent graduate seeking opportunity\" (weak)

Generate 3 subject line variations. Return ONLY a JSON array of strings, nothing else.
'''

EMAIL_BODY_PROMPT = '''You are an expert email writer helping job seekers craft personalized, genuine outreach emails.

RECIPIENT INFO:
- Name: {recipient_first_name} {recipient_last_name}
- Title: {recipient_title}
- Company: {recipient_company}

SENDER INFO:
- Name: {sender_name}
- Background: {sender_background}
- Key Skills: {sender_skills}
- Purpose: {purpose}
{role_info}
{context}

TONE: {tone}

STRICT RULES:
1. Keep it under 150 words (recruiters are busy)
2. Start with a specific hook (NOT \"I hope this email finds you well\")
3. Show you researched them/company (be specific, not generic)
4. Highlight ONE relevant achievement or skill
5. Clear call-to-action
6. NO cliches: \"passionate\", \"rockstar\", \"ninja\", \"guru\", \"fast-paced environment\"
7. NO begging language: \"would love the opportunity\", \"please consider\"
8. Be confident but humble
9. Use active voice
10. DO NOT make up facts or projects - only use provided information

EMAIL STRUCTURE:
Paragraph 1 (2-3 sentences): Specific hook about recipient or company
Paragraph 2 (2-3 sentences): ONE relevant achievement or skill with brief context
Paragraph 3 (1-2 sentences): Clear ask and call-to-action

GOOD OPENING EXAMPLES:
- \"I saw you're hiring for [role] and noticed your team uses [tech stack]. I just built something similar handling [scale/challenge].\"
- \"Your post about [specific topic] resonated - I ran into the same issue at [company] and solved it by [brief solution].\"

BAD OPENING EXAMPLES:
- \"I hope this email finds you well.\" (generic)
- \"I am writing to express my interest...\" (formal/robotic)
- \"I am a passionate developer...\" (cliche)

Generate the email body. Return ONLY the email text, no subject line, no formatting markers.
'''

COMPLETE_EMAIL_PROMPT = '''You are an expert at writing personalized job outreach emails that get responses.

RECIPIENT:
- Name: {recipient_first_name} {recipient_last_name}
- Title: {recipient_title}
- Company: {recipient_company}
{recipient_context}

SENDER:
- Name: {sender_name}
- Email: {sender_email}
- Background: {sender_background}
- Skills: {sender_skills}
{sender_portfolio}
{sender_linkedin}
{role_info}
{context}

TONE: {tone}

TASK: Generate a complete cold outreach email (subject + body).

SUBJECT LINE RULES:
- Under 50 characters
- Specific and intriguing
- NO generic phrases
- Professional but human

BODY RULES:
- Under 150 words
- Specific hook (research-based)
- ONE key achievement
- Clear call-to-action
- NO cliches or begging language
- Active voice
- DO NOT fabricate information

OUTPUT FORMAT (JSON):
{{
  \"subject\": \"Your subject line here\",
  \"body\": \"Email body here\\n\\nBest,\\n{sender_name}\"
}}

Return ONLY valid JSON, nothing else.
'''

def get_subject_prompt(
    recipient_first_name: str,
    recipient_company: str,
    recipient_title: str,
    sender_name: str,
    sender_role: str,
    purpose: str,
    context: str = None
) -> str:
    context_str = f'Additional context: {context}' if context else ''
    return SUBJECT_LINE_PROMPT.format(
        recipient_first_name=recipient_first_name,
        recipient_title=recipient_title,
        recipient_company=recipient_company,
        sender_name=sender_name,
        sender_role=sender_role,
        purpose=purpose,
        context=context_str
    )

def get_body_prompt(
    recipient_first_name: str,
    recipient_last_name: str,
    recipient_title: str,
    recipient_company: str,
    sender_name: str,
    sender_background: str,
    sender_skills: List[str],
    purpose: str,
    role_interested_in: str = None,
    context: str = None,
    tone: str = 'professional'
) -> str:
    role_info = f'Role interested in: {role_interested_in}' if role_interested_in else ''
    context_str = f'Additional context: {context}' if context else ''
    skills_str = ', '.join(sender_skills)
    
    return EMAIL_BODY_PROMPT.format(
        recipient_first_name=recipient_first_name,
        recipient_last_name=recipient_last_name or '',
        recipient_title=recipient_title or 'Hiring Manager',
        recipient_company=recipient_company,
        sender_name=sender_name,
        sender_background=sender_background,
        sender_skills=skills_str,
        purpose=purpose,
        role_info=role_info,
        context=context_str,
        tone=tone
    )

def get_complete_prompt(
    recipient_first_name: str,
    recipient_last_name: str,
    recipient_title: str,
    recipient_company: str,
    sender_name: str,
    sender_email: str,
    sender_background: str,
    sender_skills: List[str],
    sender_portfolio: str = None,
    sender_linkedin: str = None,
    role_interested_in: str = None,
    context: str = None,
    tone: str = 'professional'
) -> str:
    recipient_context = ''
    sender_portfolio_str = f'Portfolio: {sender_portfolio}' if sender_portfolio else ''
    sender_linkedin_str = f'LinkedIn: {sender_linkedin}' if sender_linkedin else ''
    role_info = f'Role interested in: {role_interested_in}' if role_interested_in else ''
    context_str = f'Additional context: {context}' if context else ''
    skills_str = ', '.join(sender_skills)
    
    return COMPLETE_EMAIL_PROMPT.format(
        recipient_first_name=recipient_first_name,
        recipient_last_name=recipient_last_name or '',
        recipient_title=recipient_title or 'Hiring Manager',
        recipient_company=recipient_company,
        recipient_context=recipient_context,
        sender_name=sender_name,
        sender_email=sender_email,
        sender_background=sender_background,
        sender_skills=skills_str,
        sender_portfolio=sender_portfolio_str,
        sender_linkedin=sender_linkedin_str,
        role_info=role_info,
        context=context_str,
        tone=tone
    )
