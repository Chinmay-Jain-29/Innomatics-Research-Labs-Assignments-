from langchain_core.output_parsers import JsonOutputParser
from prompts.explain_prompt import explain_prompt

def get_explanation_chain(llm):
    """
    Creates an LCEL chain for generating an explanation of the final score.
    """
    chain = explain_prompt | llm | JsonOutputParser()
    return chain
