# AI Resume Screening System

This repository contains an end-to-end AI-powered Resume Screening System utilizing LangChain (LCEL), Groq LLM, and LangSmith. It automates the extraction, matching, scoring, and evaluation explanation for candidate resumes against a job description.

## Architecture & Steps

1. **Extraction**: Extracts "skills", "experience", and "tools" from the unstructured resume text and outputs strict JSON using a few-shot Prompt Template.
2. **Matching**: Compares extracted parameters against the job description to identify matched skills, missing skills, and a match percentage.
3. **Scoring**: Computes a final fitness score out of 100 based on the match evaluation.
4. **Explanation**: Summarizes reasoning, strengths, and weaknesses for the candidate.

## Setup Instructions

1. **Install Requirements**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables**:
   Copy `.env.example` to `.env` and fill in your keys:
   - `GROQ_API_KEY`: Get this from Groq Console.
   - `LANGCHAIN_API_KEY`: Get this from LangSmith.

3. **Run the Application**:
   ```bash
   python main.py
   ```
   This will sequentially process 3 demo candidates (Strong, Average, Weak).

## Debugging and LangSmith Tracing

### LangSmith Integration
Because `LANGCHAIN_TRACING_V2=true` is set, all executions are automatically traced. 
We've utilized `langchain_core.runnables.RunnableConfig` to add metadata tags (e.g., `["strong", "resume_screening"]`) to each run, making filtering inside LangSmith extremely clean. 

### Debugging Demo ("Intentional Failure")
In the `main.py` file, we added the `run_debug_demo()` function which deliberately uses an incorrect prompt.
**What went wrong**: 
The bad prompt intentionally commands the LLM to output a raw string list instead of the required JSON, AND it asks it to hallucinate "Quantum Computing". 
As a result, `JsonOutputParser` throws an `OutputParserException` when it tries to parse a raw string representing a Python list into a JSON dictionary.

**How to debug with LangSmith**:
1. Open your LangSmith Tracing Dashboard.
2. Filter the traces by the tag `debug_demo`.
3. You will see a trace highlighted in RED (indicating an error).
4. Click into the trace. LangSmith perfectly visualizes the Directed Acyclic Graph (DAG) for LCEL pipeline. 
5. Under `ChatGroq`, you will see the LLM successfully returned a raw bulleted list. 
6. Under `JsonOutputParser`, you will see the exact traceback indicating why the parsing failed (expected a JSON array/object, received unstructured text). This explicitly shows that the prompt engineering rules (JSON constraints) were broken, requiring a fix in the `PrompTemplate` step.
