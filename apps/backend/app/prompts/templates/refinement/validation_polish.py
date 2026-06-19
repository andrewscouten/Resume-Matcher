"""Validation and polish prompt for the refinement pipeline."""

REFINEMENT_VALIDATION_POLISH_PROMPT = """Review and polish this resume content. Remove any AI-sounding language and ensure all content is truthful.

REMOVE or REPLACE:
- Buzzwords: "spearheaded", "synergy", "leverage", "orchestrated", etc.
- Em-dashes (use commas or semicolons instead)
- Overly formal language: "utilized" -> "used", "endeavored" -> "worked"
- Generic filler: "in order to" -> "to"
- Filler phrases: "proven experience in", "hands-on experience", "hands-on expertise", "demonstrated expertise", "proven track record", "results-driven", "passionate about", "excels at", "strong background in", "skilled at", "proficient in", "adept at", "well-versed in", "expertise in", "drive organizational decisions", "for diverse audiences"
- Empty intensifiers used without specific detail: "complex", "critical", "diverse", "large-scale", "comprehensive", "robust", "scalable", "innovative", "cutting-edge", "advanced", "extensive", "significant", "key", "essential", "dynamic", "strategic", "sophisticated", "high-impact", "mission-critical". Replace with a concrete detail from the resume or drop entirely.

VERIFY:
- All skills exist in the master resume
- All certifications exist in the master resume
- No fabricated metrics or achievements

Resume to polish:
{resume}

Master resume (verify all claims against this):
{master_resume}

Output the polished resume JSON. Return ONLY valid JSON."""
