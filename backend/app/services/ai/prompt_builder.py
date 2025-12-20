from typing import Optional, List

class VaradStylePromptBuilder:
    """
    Build prompts that generate emails in Varad's winning style
    Based on analysis of emails that got replies from hiring managers
    """
    
    @staticmethod
    def build_killer_subject_line_prompt(
        recipient_name: str,
        recipient_company: str,
        recipient_title: Optional[str] = None,
        company_mission: Optional[str] = None,
        role_name: Optional[str] = None
    ) -> str:
        """
        Generate subject lines in Varad's style - intriguing, research-backed, not generic
        
        Examples of what works:
        - "Not another resume blast ;) — reaching out with intent"
        - "I Know What You're Building at SoFi"
        - "Turning real-world movement into software that actually pays off"
        """
        
        context = f"""Generate 3 highly engaging, non-generic email subject lines for a cold outreach to {recipient_name}"""
        
        if recipient_title:
            context += f", {recipient_title}"
        context += f" at {recipient_company}"
        
        if company_mission:
            context += f"\n\nCompany mission/focus: {company_mission}"
        
        if role_name:
            context += f"\nRole applying for: {role_name}"
        
        prompt = f"""{context}

REQUIREMENTS - CRITICAL:
1. DO NOT use generic phrases like:
   - "Application for [role]"
   - "Interested in [company]"
   - "Following up"
   - "Quick question"
   
2. INSTEAD, use patterns that show research and intrigue:
   - Reference what they're actually building (specific tech/problem)
   - Use conversational hooks ("I know what you're building...")
   - Show you understand their challenge at a deep level
   - Make it personal but professional
   - Can use a tasteful emoji or punctuation for personality ;)

3. Examples of GOOD subject lines (for inspiration, don't copy):
   - "Not another resume blast ;) — reaching out with intent"
   - "I Know What You're Building at [Company]"
   - "Turning [their actual problem] into [their actual solution]"
   - "[Specific tech they use] + [specific problem they solve] — let's talk"

4. Keep under 60 characters when possible

Return ONLY a JSON array of 3 subject lines:
["Subject 1", "Subject 2", "Subject 3"]
"""
        return prompt
    
    @staticmethod
    def build_varad_style_email_prompt(
        # Recipient info
        recipient_first_name: str,
        recipient_company: str,
        recipient_title: Optional[str] = None,
        
        # Job/Company context
        role_name: Optional[str] = None,
        role_url: Optional[str] = None,
        company_mission: Optional[str] = None,
        company_tech_stack: Optional[List[str]] = None,
        company_notable_clients: Optional[List[str]] = None,
        
        # Sender info
        sender_name: str = "Varad Nair",
        sender_email: str = "vnairusa30@gmail.com",
        sender_phone: str = "+1 (657)-767-9035",
        sender_years_exp: str = "4+",
        sender_core_skills: Optional[List[str]] = None,
        sender_portfolio: str = "https://varadnair30.github.io/my_portfolio/",
        sender_linkedin: str = "https://linkedin.com/in/varad-nair",
        sender_calendar: str = "https://calendar.app.google/uLbvFdAuXgt4m41EA",
        
        # Customization
        specific_passion_point: Optional[str] = None,
        technical_hook: Optional[str] = None,
        
    ) -> str:
        """
        Generate a complete email in Varad's winning style
        
        Structure that works:
        1. Specific hook about what they're building
        2. Technical credibility with system thinking
        3. "I KNOW WHAT YOU WANT" section (killer move)
        4. Emotional connection to the mission
        5. Clear CTA with calendar link
        """
        
        # Build context
        context = f"""
RECIPIENT: {recipient_first_name}"""
        
        if recipient_title:
            context += f", {recipient_title}"
        context += f" at {recipient_company}"
        
        if role_name:
            context += f"\nROLE: {role_name}"
        if role_url:
            context += f"\nROLE URL: {role_url}"
        
        # Company details
        if company_mission:
            context += f"\n\nCOMPANY MISSION/FOCUS:\n{company_mission}"
        
        if company_tech_stack:
            context += f"\n\nTECH STACK: {', '.join(company_tech_stack)}"
        
        if company_notable_clients:
            context += f"\nNOTABLE CLIENTS: {', '.join(company_notable_clients)}"
        
        # Sender context
        sender_context = f"""
SENDER: {sender_name}
EXPERIENCE: {sender_years_exp} years as software engineer
"""
        
        if sender_core_skills:
            sender_context += f"CORE SKILLS: {', '.join(sender_core_skills[:8])}"
        
        sender_context += f"""
PORTFOLIO: {sender_portfolio}
LINKEDIN: {sender_linkedin}
CALENDAR: {sender_calendar}
EMAIL: {sender_email}
PHONE: {sender_phone}
"""
        
        if specific_passion_point:
            sender_context += f"\nPASSION POINT: {specific_passion_point}"
        
        if technical_hook:
            sender_context += f"\nTECHNICAL HOOK: {technical_hook}"
        
        prompt = f"""{context}

{sender_context}

GENERATE AN EMAIL IN THIS EXACT STYLE:

STRUCTURE (CRITICAL - FOLLOW THIS):

1. OPENING HOOK (2-3 sentences):
   - Start with "Hi [Name],"
   - Say something like "Reaching out because [specific thing about role] didn't just look interesting — it [felt/clicked/sparked something specific]"
   - Show you understand WHAT they're building (be specific - mention tech, problem, or impact)
   - Example: "Reaching out because the Software Engineer – Infrastructure role at Baseten didn't just look interesting — it genuinely clicked. Any company can say they 'power AI,' but Baseten is one of the few actually enabling the frontier: running real workloads, real inference, real customers who ship daily."

2. ONE-CLICK PORTFOLIO LINK:
   "And here's my website, one click: {sender_portfolio}"

3. BRIEF INTRO (2 sentences):
   - "I'm {sender_name} — a [role] with [years] years..."
   - List 3-5 SPECIFIC technical things you've built (not just skills)
   - Example: "I've shipped CI/CD pipelines, event-driven systems, Kubernetes workloads, monitoring layers, and real-time data flows"

4. "I KNOW WHAT YOU WANT!" SECTION (THIS IS KEY):
   - Literally use the heading "I KNOW WHAT YOU WANT!"
   - Start with: "You're not looking for someone who just [generic skill]. You want someone who..."
   - Describe 2-3 specific capabilities they actually need
   - Show you understand the REAL challenge at a systems level
   - Example: "You're not looking for someone who just 'knows Python' or can containerize a service. You want someone who can think in systems. Someone comfortable in ambiguity, who can debug a gnarly k8s issue in the morning, optimize model deployment paths in the afternoon..."
   - End with: "That's the environment where I do my best work :)"

5. JOB APPLICATION STATEMENT:
   "I'm applying for the {role_name or 'role'} at {recipient_company}"
   If role_url provided: "(link for reference): {role_url}"

6. ENTHUSIASM + CTA (2-3 sentences):
   - Express genuine excitement about contributing
   - Mention 2-3 specific things you'd do in the role
   - Ask for 15-20 min conversation
   - Provide calendar link: "You can grab any slot that works for you: {sender_calendar}"

7. SIGNATURE:
   Warmly,
   {sender_name}
   {sender_email} | {sender_phone}
   LinkedIn | Portfolio (as hyperlinks)

TONE REQUIREMENTS:
- Confident but not arrogant
- Technical but not showing off
- Enthusiastic but genuine (use phrases like "that's the kind of X that makes you Y")
- Show systems thinking, not just skill listing
- Use casual punctuation occasionally (colons, dashes, parentheses for natural flow)
- Sound like a REAL person, not corporate speak

LENGTH: 300-400 words max (shorter is better if it packs the same punch)

CRITICAL ELEMENTS TO INCLUDE:
1. Specific mention of what they're building/their tech/their impact
2. The "I KNOW WHAT YOU WANT" section (this is the secret weapon)
3. Evidence of systems thinking (not just "I know React", but "I've built X that did Y")
4. Genuine emotional connection to the mission
5. Calendar link for easy response

DO NOT:
- Use generic phrases like "I'm excited to apply"
- List skills without context
- Write long paragraphs (keep it scannable)
- Sound like every other applicant

OUTPUT FORMAT (JSON):
{{
  "subject": "One killer subject line that shows you researched them",
  "body": "Complete email following the structure above",
  "key_hook": "The one sentence that summarizes why this email will work"
}}

Return ONLY valid JSON, no markdown formatting.
"""
        return prompt

# Wrapper class to maintain compatibility with existing code
class PromptBuilder:
    """Wrapper class for backward compatibility"""
    
    @staticmethod
    def build_subject_line_prompt(
        recipient_name: str,
        recipient_company: str,
        recipient_title: Optional[str] = None,
        sender_name: str = "",
        sender_role: Optional[str] = None,
        purpose: str = "job_inquiry",
        company_mission: Optional[str] = None,
        role_name: Optional[str] = None
    ) -> str:
        """Use Varad's killer style for subject lines"""
        return VaradStylePromptBuilder.build_killer_subject_line_prompt(
            recipient_name=recipient_name,
            recipient_company=recipient_company,
            recipient_title=recipient_title,
            company_mission=company_mission,
            role_name=role_name
        )
    
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
        tone: str = "professional",
        # NEW PARAMS for Varad style
        role_url: Optional[str] = None,
        company_mission: Optional[str] = None,
        company_tech_stack: Optional[List[str]] = None,
        company_notable_clients: Optional[List[str]] = None,
        sender_phone: Optional[str] = None,
        sender_calendar: Optional[str] = None,
        specific_passion_point: Optional[str] = None,
        technical_hook: Optional[str] = None,
    ) -> str:
        """Use Varad's winning style for complete emails"""
        
        return VaradStylePromptBuilder.build_varad_style_email_prompt(
            recipient_first_name=recipient_first_name,
            recipient_company=recipient_company,
            recipient_title=recipient_title,
            role_name=role_interested_in,
            role_url=role_url,
            company_mission=company_mission,
            company_tech_stack=company_tech_stack,
            company_notable_clients=company_notable_clients,
            sender_name=sender_name,
            sender_email=sender_email or "vnairusa30@gmail.com",
            sender_phone=sender_phone or "+1 (657)-767-9035",
            sender_years_exp="4+",
            sender_core_skills=sender_skills,
            sender_portfolio=sender_portfolio or "https://varadnair30.github.io/my_portfolio/",
            sender_linkedin=sender_linkedin or "https://linkedin.com/in/varad-nair",
            sender_calendar=sender_calendar or "https://calendar.app.google/uLbvFdAuXgt4m41EA",
            specific_passion_point=specific_passion_point,
            technical_hook=technical_hook,
        )
