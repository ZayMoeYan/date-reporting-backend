from google.generativeai import GenerativeModel

model = GenerativeModel("gemini-2.5-flash")  # Adjust if you are using SDK wrapper

def validate_report_capability(report_type: str, columns: list[str]) -> dict:
   
    prompt = f"""
                You are a data-analysis assistant.

                A user has requested a report of type: **{report_type}**

                The dataset contains the following columns:
                {columns}

                Your task:
                1. Decide whether this dataset contains enough suitable columns to generate the requested report.
                2. Return ONLY a JSON object with:
                - "can_generate": true/false
                - "reason": explanation (1 short sentence)

                Rules:
                - If the user asks for something requiring columns that do not exist, return false.
                - If the dataset clearly supports the requested analysis, return true.
                - Do NOT invent columns that don’t exist.
                - Keep the reason very brief.
            """

    result = model.generate_content(prompt)

    text = result.text.strip().strip("`").replace("json", "").strip()

    import json
    try:
        return json.loads(text)
    except:
    
        return {
            "can_generate": False,
            "reason": "Model response was invalid JSON."
        }
