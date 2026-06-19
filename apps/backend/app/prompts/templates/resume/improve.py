"""Keyword-enhancement diff prompt.

Used when the user picks "Keyword enhance" mode in the improve flow. The prompt
weaves JD keywords into existing bullets where the resume already supports them
and may rephrase bullets, but does not invent new ones. The other two strategies
have their own dedicated prompts: ``nudge.py`` (most conservative) and
``full_tailor.py`` (most aggressive).
"""

RESUME_IMPROVE_PROMPT ="""Given this resume and job description, output a JSON object with targeted changes to better align the resume with the job.

RULES:
1. Only modify content — never change names, companies, dates, institutions, or degrees
2. Do not invent metrics or achievements not supported by the original resume text
3. Do not add new work entries, education entries, or project entries
4. Weave in relevant keywords where evidence already exists. You may rephrase bullets but do not add new ones.
5. Each change MUST include the original text (copied exactly) so it can be verified
6. For each change, explain WHY it helps match the job description
7. Generate all new text in {output_language}
8. Do not use em dash characters
9. Keep changes minimal and targeted — do not rewrite content that already aligns well
10. Exception to rule 2: you may add a skill only if it appears in the verified skill targets below
11. Improve work and project bullets around the verified skill targets when the original text supports that alignment
12. Preserve all hyperlinks verbatim. If the original text contains a markdown link ([text](url)), the rewritten value must include that exact link unchanged. Never drop, shorten, or alter a URL.

WRITING STYLE — apply to all generated text (bullets, summary, reason fields, strategy_notes)
- No em dashes.
- No hollow openers: "Certainly!", "Sure!", "Absolutely!", "Great question!", or any similar affirmation.
- No self-announcing meta-commentary: "Here's a clear, practical rundown:", "Short answer:", "Bottom line:", "Honestly,", "My honest take:", "Here's the thing:".
- No "It's X, not Y" constructions.
- Do not wrap rephrased ideas in unnecessary quotation marks (e.g., a "red flag" pattern).
- No emojis.
- Do not use filler transitions like "just", "simply", "basically", "literally" at the start of a phrase.
- Prefer direct phrasing over stating what you are or are not going to do.
- Banned summary/bullet phrases: "proven experience in", "proven track record", "hands-on experience", "hands-on expertise", "real-world", "demonstrated expertise", "results-driven", "passionate about", "excels at", "strong background in", "comfortable with", "fast-paced", "collaborative environment", "skilled at", "proficient in", "adept at", "well-versed in", "expertise in", "drive organizational decisions", "drive business outcomes", "ensuring accuracy and consistency", "for diverse audiences", "in a dynamic environment".
- Empty intensifiers — delete adjectives that sound impressive but add no facts: "complex", "critical", "diverse", "large-scale", "comprehensive", "robust", "scalable", "innovative", "cutting-edge", "state-of-the-art", "advanced", "extensive", "significant", "key", "essential", "dynamic", "strategic", "sophisticated", "high-impact", "high-quality", "mission-critical". Replace with a specific detail from the resume (name the system, the scale, the domain) or drop the word entirely.

DATES AND ONGOING STATUS:
- Today's date is {current_date}. Entries may carry a boolean "current" flag (and the resume a "_meta.current_date" anchor). "current": true means a job/project is ongoing, or for education that the degree is in progress and the candidate is currently enrolled. A degree is also in progress when its end date is later than today.
- You may make the summary reflect an in-progress degree by describing the candidate as a current student at that level in that EXACT field (e.g. "Master's student in Computer Science"). This is supported by the resume, not invented. Copy the field of study verbatim from the degree - never swap "Computer Science" for "software engineering" or similar.

SUMMARY QUALITY — when you rewrite the summary
- Lead with identity and level, framed toward the target role; do not promote a title or level the candidate does not hold.
- Front-load the single strongest JD-relevant qualification; favor concrete specifics, reuse only numbers already in the resume — never invent a metric.
- Implied first person (no "I"/"me"/"my"), describe value offered not goals sought, 3–4 tight sentences.
- Before finalizing, strip: (1) banned phrases — "proven experience in", "hands-on experience", "hands-on expertise", "real-world", "demonstrated expertise", "proven track record", "results-driven", "passionate about", "excels at", "strong background in", "comfortable with", "comfortable working remotely", "collaborative environment", "fast-paced", "rapid prototyping", "iterative refinement", "systems thinking", "cross-functional", "skilled at", "proficient in", "adept at", "well-versed in", "expertise in", "drive organizational decisions", "drive business outcomes", "for diverse audiences" — they add no information; (2) empty intensifiers — "complex", "critical", "diverse", "large-scale", "comprehensive", "robust", "scalable", "innovative", "advanced", "extensive", "significant", "key", "essential", "dynamic", "strategic", "sophisticated" — replace with a specific detail or drop; (3) any capability claim not anchored to a named project, system, or outcome in the resume; (4) baseline skills assumed for the role — leave those to the skills section.
- Differentiation test: if this summary could appear unmodified on another candidate's resume for the same role, rewrite it with specifics that could only describe this person.

BULLET QUALITY — when you rephrase a work or project bullet:
- Lead with a strong, specific action verb. Replace weak lead-ins ("Responsible for", "Duties included", "Helped with", "Worked on", "Assisted with") with the action itself.
- Favor an action + result shape: name what was done and the outcome or impact it produced, not just the task. Make the "so what" explicit wherever the original supports it.
- Surface concrete scope, scale, volume, or frequency the resume already shows; never invent a metric (see rule 2). If no number is supported, state the scope in words.
- Use active voice and implied first person with no pronouns ("Led X", not "I led X" and not the passive "X was led"). Keep past tense for completed roles and present tense for a current/ongoing role, consistent within each entry.
- Vary the opening verb across bullets within the same entry; do not repeat the same opening verb on consecutive bullets.
- Cut filler ("various tasks", "as needed", "fast-paced environment") and empty intensifiers ("complex", "critical", "diverse", "large-scale", "comprehensive", "robust", "advanced", "significant", "key", "essential", "strategic"). Replace with a concrete detail or drop entirely. Keep each bullet to one or two lines.

PATHS you can target:
- "summary" — the resume summary text
- "workExperience[i].description[j]" — a specific bullet (i = entry index, j = bullet index)
- "workExperience[i].description" — append a new bullet (action: "append")
- "personalProjects[i].description[j]" — a specific project bullet
- "personalProjects[i].description" — append a new project bullet
- "additional.technicalSkills" — reorder the skills list (action: "reorder") or add one verified skill (action: "add_skill"). When reordering, cluster topically related skills adjacent to each other (you choose the clusters based on the skills present, e.g. languages together, frameworks together, databases together) and lead each cluster with its most JD-relevant entries; when relevance is equal, order by depth of use.

Do NOT target: personalInfo, dates/years, company names, education, customSections.

Keywords to emphasize (only if already supported by resume content):
{job_keywords}

Verified skill targets:
{skill_targets}

Job Description:
{job_description}

Original Resume:
{original_resume}

Output this exact JSON format, nothing else:
{{
  "changes": [
    {{
      "path": "workExperience[0].description[1]",
      "action": "replace",
      "original": "the exact original text at this path",
      "value": "the improved text",
      "reason": "why this change helps"
    }},
    {{
      "path": "summary",
      "action": "replace",
      "original": "the current summary text",
      "value": "the improved summary",
      "reason": "why this change helps"
    }},
    {{
      "path": "additional.technicalSkills",
      "action": "reorder",
      "original": null,
      "value": ["most relevant skill first", "then next", "..."],
      "reason": "reordered to prioritize JD-relevant skills"
    }},
    {{
      "path": "additional.technicalSkills",
      "action": "add_skill",
      "original": null,
      "value": "verified skill target missing from the skills list",
      "reason": "added verified JD skill for review"
    }}
  ],
  "strategy_notes": "brief summary of the tailoring approach"
}}"""
