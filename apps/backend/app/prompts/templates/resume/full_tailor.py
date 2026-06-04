"""Full-tailoring diff prompt.

Used when the user picks "Full tailor" mode in the improve flow. This mode
permits aggressive rewriting and reframing of the resume to align with the
job description, bounded by a plausibility floor that forbids cross-domain
fabrication. User guidance (appended at runtime by `_append_user_guidance`
in `app.services.improver`) is authoritative on voice, tone, audience, and
how aggressively to bend.

Forked from `RESUME_IMPROVE_PROMPT` so the full-tailor rules can state their
own constraints coherently instead of overriding rules in a shared scaffold.
"""

RESUME_FULL_TAILOR_PROMPT = """Tailor this resume to the job description. Output a JSON object with targeted changes, nothing else.

FULL TAILOR MODE
The user has opted in to bending the resume toward the job description. User guidance (if provided at the end of the prompt) is authoritative on voice, framing, tone, audience, and how aggressively to bend. Honor it.

WHAT YOU MAY DO
- Rewrite bullets: change wording, voice, action verbs, sentence structure, and framing. Rewrites must REPLACE the original (action: "replace"). Never produce output that is the original text followed by additional clauses tacked on.
- Add new bullets that elaborate on or reframe work the candidate actually did.
- Reframe academic/research work in industry terms (or vice versa) when guidance supports it.
- Include adjacent skills, tools, or vocabulary a candidate with this background would plausibly have. "Framing" means voice and emphasis, not relabeling what the work was (see PLAUSIBILITY FLOOR).
- Reframe the SUMMARY's lead identity when guidance signals a different audience or career stage. The lead noun is repositionable using framing supported by guidance and the resume. Do not invent a status not in the resume; an in-progress degree is a real status, not an invented one — see DATES AND ONGOING STATUS.
- Rename an existing skill to a closely related verified target when the rename is a generalization, specialization, or near-synonym (e.g., "MySQL" -> "SQL"). Use action "rename_skill". Do not swap to an unrelated skill.
- Remove an existing skill when it has no plausible relevance to the JD AND removing it does not strip credible coverage. Example: "Forklift Certified" on a Full-Stack Engineer resume. Use action "remove_skill".
- Promote broad domain concepts (e.g. "Machine Learning", "Distributed Systems", "Prompt Engineering") from the skills list into prose where they can be evidenced by real work. Pair a "remove_skill" with one or more "replace"/"append" changes that surface the concept against specific work. Never remove a broad concept without surfacing it elsewhere in the same change set.

SUMMARY QUALITY — when you rewrite the summary
BUILD:
- Sentence 1: candidate identity + level + single strongest JD-relevant qualification — use facts from the resume, not aspirations.
- Sentences 2–3: two or three specific capabilities or outcomes, each anchored to a named system, project, result, or domain from the resume.
- Implied first person (no "I"/"me"/"my"), describe value offered not goals sought. One paragraph, 3–4 tight sentences.

STRIP — run each check before finalizing:
1. Banned phrases — delete any of these on sight: "hands-on experience", "real-world", "demonstrated expertise", "proven track record", "results-driven", "passionate about", "excels at", "strong background in", "comfortable with", "comfortable working remotely", "collaborative environment", "fast-paced", "rapid prototyping", "iterative refinement", "systems thinking", "cross-functional". They carry no information.
2. Unanchored abstractions — cut any capability claim you cannot link to a named project, system, or outcome in the resume. If you cannot point to it, cut it.
3. Table stakes — do not claim baseline skills assumed for the role. Say something specific about depth or scale, or leave it to the skills section.
4. Differentiation test — could this summary appear unmodified on another candidate's resume for the same role? If yes, rewrite using specifics that could only describe this person.

BULLET QUALITY — when you rewrite or add a work/project bullet
- Lead with a strong, specific action verb (Built, Led, Designed, Shipped, Automated, Reduced). Never open with "Responsible for", "Duties included", "Helped with", "Worked on", or "Assisted with".
- Action + what + result: name what was done and the outcome it produced. Make the "so what" explicit wherever the resume supports it.
- Quantify with scope, scale, or frequency already in the resume. Never invent a number; if none is supported, describe scope in words.
- Active voice, implied first person, no pronouns. Past tense for completed roles, present tense for current. One to two lines per bullet.
- No filler ("various tasks", "as needed", "fast-paced"). Every claim must point at real work.
- Vary the opening verb across bullets within an entry.

PLAUSIBILITY FLOOR — NEVER CROSS
- Test every JD keyword: could the work the resume explicitly describes plausibly HAVE BEEN or USED this keyword? INCLUDE it when the keyword is a mainstream instance, tool, or method of work already described (e.g. a resume stating "object detection" may name "YOLO"). Do NOT apply it when the keyword denotes a different CATEGORY of work — e.g. single-machine multithreaded code is not "distributed systems" and must not be relabeled as such. You may rewrite voice, verbs, and emphasis freely; you may not recharacterize the category of work. When a keyword fails the test, describe the work accurately and let the mismatch stand.
- Do not claim experience in a domain the candidate has no demonstrated footing in.
- Do not invent specific numeric metrics not in the original. Vague qualitative claims are fine; fabricated numbers are not.
- Do not invent named products, companies, certifications, degrees, or employers.
- Do not extend employment dates or change timelines. Copy date ranges exactly.
- Do not upgrade titles ("Intern" -> "Engineer", "Junior" -> "Senior").
- Do not remove certifications, languages, or awards. You may reorder by relevance.
- Skill removals must satisfy ALL of: clearly off-topic for the JD; not a generic baseline skill; skills section remains populated. When in doubt, reorder instead of remove.
- Do not claim native/fluent proficiency in an unlisted language.
- If user guidance pushes past this floor, follow guidance up to the floor and stop.

DATES AND ONGOING STATUS
- Today's date is {current_date}. Use it to reason about whether dated entries are ongoing or completed.
- Entries may carry a boolean "current" flag. "current": true means a role or project is ongoing; on an education entry it means the degree is IN PROGRESS and the candidate is currently enrolled.
- Treat an education entry as in progress when its "current" flag is true OR its end date is later than today.
- When an education entry is in progress, you MAY describe the candidate as a current student in that exact field (e.g., a "Master of Science in Computer Science" in progress makes them a "Master's student in Computer Science"). Copy the FIELD OF STUDY verbatim — never generalize it (do not turn "Computer Science" into "software engineering" or similar).
- Do not call an in-progress degree completed, and do not call a completed degree in progress.

FORMAT RULES
- Only modify content — never change personalInfo, names, companies, dates, institutions, or degrees.
- Each change MUST include the original text (copied exactly) at the targeted path so it can be verified.
- For each change, explain WHY it helps match the job description or honor user guidance.
- Generate all new text in {output_language}.
- Do not use em dash characters.
- For skills: only add a skill that appears in the verified skill targets below.

PATHS you can target
- "summary" - the resume summary text
- "workExperience[i].description[j]" - a specific bullet (i = entry index, j = bullet index)
- "workExperience[i].description" - append a new bullet (action: "append")
- "personalProjects[i].description[j]" - a specific project bullet
- "personalProjects[i].description" - append a new project bullet
- "additional.technicalSkills" - reorder the list (action: "reorder"), add one verified skill (action: "add_skill"), rename an existing skill (action: "rename_skill"), or remove an irrelevant skill (action: "remove_skill")

SKILL ACTION DETAILS
- "reorder": value = full reordered list. Cluster topically related skills adjacent (languages together, frameworks together, databases together, infra/tooling together). Lead each cluster with the most JD-relevant entries; when relevance is equal, order by depth of use. No category labels in the list itself.
- "add_skill": value = new skill (must appear in Verified skill targets). Include "insert_after" naming a topically adjacent existing skill. Omit only if no related skill exists.
- "rename_skill": original = existing skill exactly; value = verified-target replacement (must be a clear generalization/specialization/synonym).
- "remove_skill": original = existing skill exactly; value = null. Use sparingly.

Do NOT target: personalInfo, dates/years, company names, education, customSections.

Keywords to emphasize (emphasize ONLY where the candidate's real work already embodies the keyword; do NOT graft a keyword onto a bullet it does not truthfully describe - leaving a keyword unused is correct when the work does not support it):
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
      "value": "the rewritten text",
      "reason": "why this change helps"
    }},
    {{
      "path": "summary",
      "action": "replace",
      "original": "the current summary text",
      "value": "the rewritten summary",
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
      "insert_after": "an existing skill that is topically adjacent",
      "reason": "added verified JD skill near related skills"
    }},
    {{
      "path": "additional.technicalSkills",
      "action": "rename_skill",
      "original": "existing skill label exactly as it appears",
      "value": "verified target that generalizes/specializes the original",
      "reason": "rename narrows or broadens to match JD vocabulary"
    }},
    {{
      "path": "additional.technicalSkills",
      "action": "remove_skill",
      "original": "existing skill label exactly as it appears",
      "value": null,
      "reason": "skill is unrelated to this JD and not a generic baseline"
    }}
  ],
  "strategy_notes": "brief summary of the tailoring approach"
}}"""
