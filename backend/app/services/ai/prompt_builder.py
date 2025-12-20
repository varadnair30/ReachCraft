from typing import Optional, List


# Resume-driven profile for Varad
VARAD_PROFILE = {
    "summary": (
        "Software Engineer with 4+ years across full-stack development, "
        "cloud-native architectures, AI/ML systems, and scalable distributed solutions."
    ),  # [file:33]
    "highlights": [  # used to pick relevant examples per role
        "Architected a production RAG assistant reducing hallucinations by 40% using LangChain, BM25 + FAISS, and Gemma 2B.",
        "Built real-time multimodal AI workflows (WebSocket → Whisper STT → LLM → Stable Diffusion) with FastAPI microservices.",
        "Developed backend network automation and Kubernetes-based services that improved scalability and reliability by 40%.",
        "Designed cloud microservices and TB-scale data pipelines on AWS/Azure (Lambda, AKS, Data Factory) for analytics workloads.",
        "Delivered 10+ production-ready web applications as a freelancer using Django/Spring Boot, React/Angular, and PostgreSQL."
    ],  # [file:33]
    "strengths": [
        "systems thinking",
        "owning end-to-end pipelines from infra to UI",
        "shipping production-ready, monitored services",
        "working close to AI/ML and data workflows"
    ],  # [file:33]
    "core_stacks": [
        "Python", "Java", "Spring Boot", "Django", "FastAPI",
        "React", "Angular", "TypeScript",
        "AWS", "Azure", "GCP",
        "Docker", "Kubernetes",
        "LangChain", "FAISS", "RAG", "LLMs"
    ]  # [file:33]
}


class VaradStylePromptBuilder:
    """
    Build prompts that generate emails in Varad's winning style,
    grounded in his actual resume and experience. [file:33]
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
        Generate subject lines in Varad's style - intriguing, research-backed, not generic.
        """
        context = (
            f"Generate 3 highly engaging, non-generic email subject lines "
            f"for a cold outreach to {recipient_name}"
        )

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
   - You may use a tasteful emoji or punctuation for personality ;)


3. Examples of GOOD subject lines (for inspiration, don't copy):
   - "Not another resume blast ;) — reaching out with intent"
   - "I Know What You're Building at [Company]"
   - "Turning [their actual problem] into [their actual solution]"
   - "[Specific tech they use] + [specific problem they solve] — let's talk"


4. Keep under 60 characters when possible.


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
        Generate a complete email in Varad's winning style.

        Structure that works:
        1. Specific hook about what they're building
        2. Resume-grounded technical credibility & systems thinking
        3. "I KNOW WHAT YOU WANT" section (role-specific)
        4. Emotional connection to the mission
        5. Clear CTA with calendar link
        """

        # Build context from recipient + role
        context = f"\nRECIPIENT: {recipient_first_name}"
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

        # Sender context (resume-driven)
        sender_context = f"""
SENDER: {sender_name}
EXPERIENCE: {sender_years_exp} years as a software engineer

PROFILE SUMMARY:
{VARAD_PROFILE["summary"]}

CORE HIGHLIGHTS (pick the most relevant for this role):
- {VARAD_PROFILE["highlights"][0]}
- {VARAD_PROFILE["highlights"][1]}
- {VARAD_PROFILE["highlights"][2]}
- {VARAD_PROFILE["highlights"][3]}
- {VARAD_PROFILE["highlights"][4]}

STRENGTHS TO LEAN ON:
- {', '.join(VARAD_PROFILE["strengths"])}

CORE STACK (choose only what matches the JD):
- {', '.join(VARAD_PROFILE["core_stacks"])}
"""
        if sender_core_skills:
            sender_context += f"\nADDITIONAL SENDER SKILLS FROM INPUT:\n- {', '.join(sender_core_skills[:8])}"

        sender_context += f"""
LINKS:
- Portfolio: {sender_portfolio}
- LinkedIn: {sender_linkedin}
- Calendar: {sender_calendar}
- Email: {sender_email}
- Phone: {sender_phone}
"""

        if specific_passion_point:
            sender_context += f"\nPASSION POINT (why this company/problem resonates):\n{specific_passion_point}"
        if technical_hook:
            sender_context += f"\nTECHNICAL HOOK (specific challenge that excites Varad):\n{technical_hook}"

        prompt = f"""{context}


{sender_context}


GENERATE AN EMAIL IN THIS STYLE (BUT WITH FRESH WORDING EACH TIME):


STRUCTURE (FOLLOW THIS ORDER):

1. OPENING HOOK (2–3 sentences)
   - Start with: "Hi {recipient_first_name},"
   - Then: "Reaching out because [specific thing about this role/company] didn't just look interesting — it genuinely clicked / sparked / resonated."
   - Show you understand WHAT {recipient_company} is building and why this particular role matters.
   - Use details from the company mission, tech stack, and job description (if provided), not generic praise.

2. ONE-CLICK PORTFOLIO LINK (1 line)
   - Exactly one simple line such as:
     "And here's my website, one click: {sender_portfolio}"

3. BRIEF INTRO (2–3 sentences, RESUME-DRIVEN)
   - Start with: "I'm {sender_name} — a software engineer with {sender_years_exp} years across full-stack, cloud, and AI systems."
   - Then, based on the ROLE and COMPANY:
     - Pick 2–3 relevant highlights from the CORE HIGHLIGHTS list above (do NOT copy bullet text verbatim; paraphrase).
     - Mention only the technologies that match THIS job from CORE STACK and/or sender_core_skills.
   - This section must feel different for an AI/RAG role vs a pure infra role vs a fintech/backend role.

4. "I KNOW WHAT YOU WANT!" SECTION (3–5 sentences)
   - Include the heading exactly: "I KNOW WHAT YOU WANT!"
   - This section MUST be specific to this company and role, not generic.
   - Pattern:
     - "You're not looking for someone who just [shallow/generic skill]. You want someone who..."
     - Describe 2–3 concrete capabilities they care about based on the JD and mission
       (e.g., owning RAG retrieval paths, deploying on Kubernetes in constrained environments,
        building TB-scale data pipelines, handling defense autonomy deployments, etc.).
     - Tie those needs back to Varad's strengths and relevant highlights above.
   - Avoid reusing the exact same wording across different emails.
   - End naturally with something like:
     "That's the environment where I do my best work :)"

5. JOB APPLICATION STATEMENT (1–2 lines)
   - "I'm applying for the {role_name or 'role'} at {recipient_company}"
   - If role_url is provided, add:
     "(link for reference): {role_url}" on the next line.

6. ENTHUSIASM + CTA (2–3 sentences)
   - Express genuine excitement about contributing to their specific mission/problem space.
   - Mention 1–2 concrete ways Varad could add value in the first few months, based on the JD.
   - Ask for a 15–20 minute chat.
   - Include:
     "You can grab any slot that works for you: {sender_calendar}"

7. SIGNATURE
   Warmly,
   {sender_name}
   {sender_email} | {sender_phone}
   LinkedIn | Portfolio

TONE REQUIREMENTS:
- Confident but not arrogant.
- Technical and specific, but not buzzword-dumpy.
- Systems thinking over skill listing: focus on owning flows, pipelines, architectures.
- Genuine, human, slightly casual (you may use a smiley, parentheses, dashes).
- No corporate fluff like "Dear Sir/Madam" or "To whom it may concern".

LENGTH:
- Aim for 250–320 words.
- Prioritize clarity and punch over length.

CRITICAL ELEMENTS:
1. Company- and role-specific hook.
2. Resume-grounded intro that varies by job.
3. A unique, role-specific "I KNOW WHAT YOU WANT!" section.
4. Clear CTA with the calendar link.
5. Zero boilerplate phrases like "I am writing to express my interest in..."

OUTPUT FORMAT (JSON):
{{
  "subject": "One killer subject line that shows you actually understand their work",
  "body": "Complete email following the structure above",
  "key_hook": "One sentence that captures why this email stands out for this specific role"
}}

Return ONLY valid JSON, no markdown, no extra commentary.
"""
        return prompt


class PromptBuilder:
    """Wrapper class for backward compatibility."""

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
        """Use Varad's killer style for subject lines."""
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
        # Varad-style extras
        role_url: Optional[str] = None,
        company_mission: Optional[List[str]] = None,
        company_tech_stack: Optional[List[str]] = None,
        company_notable_clients: Optional[List[str]] = None,
        sender_phone: Optional[str] = None,
        sender_calendar: Optional[str] = None,
        specific_passion_point: Optional[str] = None,
        technical_hook: Optional[str] = None,
    ) -> str:
        """Use Varad's winning style for complete emails."""
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
