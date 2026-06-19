"""Skill target planning prompt — picks JD-relevant skills to emphasize."""

JOB_DESCRIPTION_SKILL_TARGET_PROMPT = """Build a concise skill target plan for tailoring this resume to the job.

Return ONLY a JSON object. Do not rewrite the resume.

Rules:
1. Prefer required and preferred JD skills.
2. Include existing resume skills that are highly relevant to the JD.
3. You may include JD skills that are missing from the resume skills list.
4. Do not include skills unrelated to the JD.
5. Do not include certifications.
6. Only include concrete, nameable skills: programming languages, frameworks, libraries, tools, software, platforms, or specific technologies (e.g. "PostgreSQL", "React", "Docker"). Do NOT include vague categories or soft skills such as "Relational Databases", "Problem Solving", "Communication", "Teamwork", or "Critical Thinking". When the JD references a broad category, map it to the concrete technology the candidate actually uses (e.g. "Relational Databases" -> "PostgreSQL").
7. Generate reasons in {output_language}.

Existing resume skills:
{existing_skills}

JD keywords and skills:
{job_keywords}

Job Description:
{job_description}

Resume JSON:
{original_resume}

Output this exact JSON format:
{{
  "target_skills": [
    {{
      "skill": "skill name",
      "reason": "why this skill should be emphasized"
    }}
  ],
  "strategy_notes": "brief notes for the next editing pass"
}}"""
