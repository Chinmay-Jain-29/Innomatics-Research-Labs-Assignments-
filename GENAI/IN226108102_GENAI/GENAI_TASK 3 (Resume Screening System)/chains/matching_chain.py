from langchain_core.output_parsers import JsonOutputParser
from prompts.match_prompt import match_prompt

def get_matching_chain(llm):
    """
    Creates an LCEL chain for matching extracted resume data with the job description.
    """
    chain = match_prompt | llm | JsonOutputParser()
    return chain
