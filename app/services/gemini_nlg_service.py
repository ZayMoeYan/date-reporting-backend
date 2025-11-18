from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_summary(dataset_type, report_type, result, output_language):
    prompt = f"""
            You are a professional data analyst writing a clear, natural-language report.

            Your task: write a detailed narrative summary (20–30 sentences) based fully on:
            - The dataset type: "{dataset_type}"
            - The report type requested: "{report_type}"
            - The computed result provided: {result}

            CRITICAL REQUIREMENTS (do not ignore):
            1. You MUST explicitly incorporate all three inputs — dataset_type, report_type, and result — in the reasoning and storytelling of the report.  
            - The dataset_type should influence the context (e.g., customer dataset, sales dataset, healthcare dataset, etc.).  
            - The report_type should shape the kind of insights you focus on (e.g., trend analysis, comparison report, categorical profile, performance overview).  
            - The result must be interpreted directly and accurately (no invented numbers or columns).

            2. Language:
            - {output_language}

            3. The summary MUST be written in natural everyday language.
            - No technical statistical terms allowed, including mean, median, variance, standard deviation, max, min, quartiles, percentiles, describe(), or similar schema/summary terminology.
            - Do not mention column names unless clearly present inside the "result".
            - Never reference how the data was processed or how calculations were performed.

            4. Tone and style:
            - Professional, analytic, clear.
            - No greetings, no filler phrases, no fluff.
            - Do not provide titles or section headers.
            - Do not repeat the report_type as a header or label.

            5. Every insight must be grounded **only** in the values found inside "result".
            - No invented values.
            - If result provides limited information, expand only on what can be logically inferred.

            Write a complete report following all rules above.
            """

    resp = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return resp.text.strip()

