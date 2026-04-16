from langchain_core.output_parsers import JsonOutputParser
from prompts.score_prompt import score_prompt

def get_scoring_chain(llm):
    """
    Creates an LCEL chain for scoring the match results.
    """
    chain = score_prompt | llm | JsonOutputParser()
    return chain
