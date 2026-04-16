from langchain_core.output_parsers import JsonOutputParser
from prompts.extract_prompt import extract_prompt

def get_extraction_chain(llm):
    """
    Creates an LCEL chain for extracting information from a resume.
    Uses the provided LLM and expects structured JSON output.
    """
    # Create the LCEL pipeline: prompt -> llm -> json parser
    chain = extract_prompt | llm | JsonOutputParser()
    return chain
