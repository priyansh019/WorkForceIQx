RECRUITMENT_ANALYSIS_PROMPT = """
Analyze candidate-job alignment using explicit skills, experience, semantic fit, resume evidence, and missing or unclear requirements.
Do not use protected characteristics. Do not make a hiring decision.
Return structured JSON with skill_alignment, experience_alignment, semantic_alignment, matched_skills, missing_or_unclear_skills, evidence, interview_topics, and explanation.
"""

