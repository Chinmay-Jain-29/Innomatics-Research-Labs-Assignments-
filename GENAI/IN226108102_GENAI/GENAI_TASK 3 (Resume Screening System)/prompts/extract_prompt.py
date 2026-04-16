from langchain_core.prompts import PromptTemplate

# Prompt to extract skills, experience, and tools from the resume
# We use a few-shot example to guide the model
extract_template = """You are an expert technical recruiter and resume analyzer.
Your task is to extract skills, experience details, and tools/technologies from the provided resume text.

IMPORTANT RULES:
1. Do NOT assume any skill not explicitly mentioned in the text.
2. Calculate total years of experience if possible, or extract the overall experience text.
3. Your output MUST be in structured JSON format with the following keys exactly: "skills", "experience", "tools".

--- Few-Shot Example ---
Resume: 
"Software engineer with 5 years of experience. Expert in Python, Java, and C++. Worked with AWS and Docker. Used Git for version control."
Expected JSON Output:
{{
  "skills": ["Software Engineering"],
  "experience": "5 years",
  "tools": ["Python", "Java", "C++", "AWS", "Docker", "Git"]
}}
------------------------

Resume to analyze:
{resume_text}

JSON Output:"""

extract_prompt = PromptTemplate(
    input_variables=["resume_text"],
    template=extract_template
)
