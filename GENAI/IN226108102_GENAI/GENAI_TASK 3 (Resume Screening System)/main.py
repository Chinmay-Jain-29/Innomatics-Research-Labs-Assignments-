import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check context
if not os.getenv("GROQ_API_KEY"):
    raise ValueError("Please set GROQ_API_KEY in your .env file.")

from langchain_groq import ChatGroq
from langchain_core.runnables import RunnableConfig
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from chains.extraction_chain import get_extraction_chain
from chains.matching_chain import get_matching_chain
from chains.scoring_chain import get_scoring_chain
from chains.explanation_chain import get_explanation_chain

# Initialize Groq LLM
# Using llama3-8b-8192 for fast processing, or mixtral-8x7b-32768
# ensuring json_mode is NOT strictly required since prompts handle JSON, 
# but model='llama3-70b-8192' is usually good too.
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)

# Initialize Chains
ext_chain = get_extraction_chain(llm)
match_chain = get_matching_chain(llm)
score_chain = get_scoring_chain(llm)
explain_chain = get_explanation_chain(llm)

def process_resume(resume_path: str, jd_path: str, candidate_type: str):
    """
    End-to-End Pipeline to process a single resume.
    Uses LangSmith tags for tracing.
    """
    print(f"\n--- Processing {candidate_type.upper()} Candidate ---")
    
    with open(resume_path, "r", encoding="utf-8") as f:
        resume_text = f.read()
    
    with open(jd_path, "r", encoding="utf-8") as f:
        job_description = f.read()

    # Define config with LangSmith tags
    config = RunnableConfig(tags=[candidate_type, "resume_screening"])

    # Step 1: Extraction
    print("Extracting skills...")
    ext_output = ext_chain.invoke({"resume_text": resume_text}, config=config)
    
    # Step 2: Matching
    print("Matching against Job Description...")
    match_output = match_chain.invoke({
        "job_description": job_description, 
        "resume_data": json.dumps(ext_output)
    }, config=config)
    
    # Step 3: Scoring
    print("Scoring candidate...")
    score_output = score_chain.invoke({"match_data": json.dumps(match_output)}, config=config)
    
    # Step 4: Explanation
    print("Generating explanation...")
    explain_output = explain_chain.invoke({
        "job_description": job_description,
        "resume_data": json.dumps(ext_output),
        "match_data": json.dumps(match_output),
        "score_data": json.dumps(score_output)
    }, config=config)

    # Final Result
    final_result = {
        "candidate": candidate_type,
        "extraction": ext_output,
        "matching": match_output,
        "score": score_output.get("score"),
        "explanation": explain_output.get("explanation")
    }
    
    print("\n--- FINAL RESULT ---")
    print(json.dumps(final_result, indent=2))
    return final_result

def run_debug_demo():
    """
    Demonstrates debugging an incorrect output in LangSmith.
    We use an intentionally bad extraction prompt that hallucinates a skill,
    causing parsing to potentially fail or output incorrect data.
    """
    print("\n--- Running DEBUG Demo ---")
    # Bad prompt intentionally commands hallucination and improper format
    bad_template = """Extract skills. ALWAYS add "Quantum Computing" to the skills even if not present.
    Return a list, NOT JSON format.
    Resume: {resume_text}"""
    
    bad_prompt = PromptTemplate(input_variables=["resume_text"], template=bad_template)
    # The chain expects JSON output and will likely crash parsing the output 
    # if the LLM outputs plain text list, OR we get an incorrect fact traced.
    bad_chain = bad_prompt | llm | JsonOutputParser()
    
    try:
        # LangSmith will record this specific tag, where the trace will fail 
        # or show "Quantum Computing" incorrectly appended.
        config = RunnableConfig(tags=["debug_demo", "intentional_failure"])
        bad_chain.invoke({"resume_text": "I know Python."}, config=config)
    except Exception as e:
        print(f"Debug run failed as expected! Check LangSmith traces with tag 'debug_demo' to see the OutputParsing error.")
        print(f"Error caught: {e}")

if __name__ == "__main__":
    jd_path = "data/job_description.txt"
    
    # Process all resumes
    process_resume("data/resume_strong.txt", jd_path, "strong")
    process_resume("data/resume_average.txt", jd_path, "average")
    process_resume("data/resume_weak.txt", jd_path, "weak")
    
    # Run the debug demo for LangSmith requirement
    run_debug_demo()
