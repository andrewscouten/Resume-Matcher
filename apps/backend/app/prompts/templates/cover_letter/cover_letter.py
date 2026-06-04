"""Cover letter generation prompt."""

COVER_LETTER_PROMPT = """Write a cover letter for this job application. It must fit on one page.

IMPORTANT: Write in {output_language}.

Job Description:
{job_description}

Candidate Resume (JSON):
{resume_data}

STRUCTURE (four paragraphs, 250-400 words total):
1. Opening — Name the role and immediately signal the strongest reason you fit it. Reference something concrete from the JD (a product, technical challenge, or domain problem). Never open with "I am writing to apply for...", "I saw your posting", or "I am interested in..."
2. Qualification paragraph — Tell the story behind one or two resume items most directly matched to the JD's stated requirements. Use the STAR shape (situation/context, action taken, result): a brief setup, what you specifically did, and the outcome it produced. Do NOT lift bullet points verbatim; the cover letter elaborates on context and impact, it does not re-list facts.
3. Company paragraph — Demonstrate you know this specific organization. Reference their product, mission, tech stack, or engineering culture. Explain why that specific aspect resonates with your background. Hollow praise like "I admire your growth" is not company research.
4. Closing — Simple availability to discuss. No desperate enthusiasm. Sign off with "Sincerely," on its own line and the candidate's full name on the next.

RULES:
- Salutation: "Dear Hiring Manager," — use actual name only if clearly stated in the JD
- Tone: Confident peer, not eager applicant
- Complement the resume, don't duplicate it — the letter adds narrative context, not a re-list of bullet points
- For technical roles: explain HOW you used the technologies from your resume — what you built, what problem it solved. Naming tools without context adds no value.
- For data science/ML roles: translate analytical results into business impact; show you can communicate technical work to non-technical stakeholders
- For entry-level and internship applications where work history is thin: build the qualification paragraph from academic projects, open-source contributions, and relevant coursework — do not force STAR narratives from absent experience
- Frame career transitions as intentional and relevant, not defensive
- Extract company name from the JD — do not use placeholders
- Do NOT invent information not in the resume
- Do NOT use em dash ("—") anywhere in the output

Output plain text only. No JSON, no markdown formatting."""
