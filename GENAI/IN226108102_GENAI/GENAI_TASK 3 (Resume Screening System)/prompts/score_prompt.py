from langchain_core.prompts import PromptTemplate

# Prompt to generate a final score based on the match details
score_template = """You are an HR Evaluation AI.
Based on the match details between a candidate's resume and a job description, compute a final score between 0 and 100.

Match Details:
{match_data}

Consider:
- High match percentage should yield a high score.
- Heavily penalize if core required skills are missing.
- Score should be an integer.

IMPORTANT rules:
Provide ONLY a valid JSON object with EXACTLY the following key:
"score" (integer)

JSON Output:"""

score_prompt = PromptTemplate(
    input_variables=["match_data"],
    template=score_template
)
