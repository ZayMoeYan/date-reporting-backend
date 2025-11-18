from google import genai
import os
from dotenv import load_dotenv
import re

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def extract_code(text: str) -> str:
    m = re.search(r"```(?:python)?\s*(.*?)```", text, re.S)
    return m.group(1).strip() if m else text.strip()

def generate_processing_code(dataset_type, report_type, schema, columns):
    prompt = f"""
    You are a Python/pandas expert. Generate Python code that computes the report.

    Dataset type: {dataset_type}
    Report type: {report_type}

    Available columns: {columns}
    Dataset schema: {schema}

    Rules:
    - Use only 'df' and 'pd'.
    - No imports.
    - No prints.
    - Do NOT modify the dataframe.
    - Store final result in ANSWER.
    - If computation is not possible, set ANSWER = None.

    Return ONLY executable Python code.
    """

    code_resp = client.models.generate_content(
        model="gemini-2.5-flash", contents=prompt
    )
    return extract_code(code_resp.text)
