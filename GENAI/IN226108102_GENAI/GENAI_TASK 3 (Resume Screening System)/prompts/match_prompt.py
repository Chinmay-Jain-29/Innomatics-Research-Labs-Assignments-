from langchain_core.prompts import PromptTemplate

# Prompt to match extracted resume details with the Job description
match_template = """You are an expert HR matching algorithm. 
Compare the extracted resume details with the job description.

Job Description:
{job_description}

Extracted Resume Details:
{resume_data}

Identify the matched skills and the missing skills based strictly on the job description requirements.
Estimate a match percentage (0-100) based on how well the candidate's skills and tools match the job requirements.

IMPORTANT rules:
Provide ONLY a valid JSON object with EXACTLY the following keys:
"matched_skills" (list of strings)
"missing_skills" (list of strings)
"match_percentage" (integer)

DO NOT include any extra text, markdown formatting like ```json, comments, or explanations outside or inside the JSON string. Ensure the JSON is strictly well-formed, using only double quotes.

JSON Output:"""

match_prompt = PromptTemplate(
    input_variables=["job_description", "resume_data"],
    template=match_template
)
