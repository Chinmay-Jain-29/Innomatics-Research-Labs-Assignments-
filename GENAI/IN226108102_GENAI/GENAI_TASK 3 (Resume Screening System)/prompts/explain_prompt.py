from langchain_core.prompts import PromptTemplate

# Prompt to generate an explanation for the score
explain_template = """You are a hiring manager explaining the evaluation results.
Given the candidate's extracted data, the match results, and the final score assigned, provide a brief but clear reasoning.

Job Description:
{job_description}

Resume Data:
{resume_data}

Match Results:
{match_data}

Final Score:
{score_data}

Provide an explanation that covers:
1. Why this score was assigned.
2. Key strengths of the candidate.
3. Key weaknesses or missing requirements.

IMPORTANT rules:
Provide ONLY a valid JSON object with EXACTLY the following key:
"explanation" (string)

JSON Output:"""

explain_prompt = PromptTemplate(
    input_variables=["job_description", "resume_data", "match_data", "score_data"],
    template=explain_template
)
