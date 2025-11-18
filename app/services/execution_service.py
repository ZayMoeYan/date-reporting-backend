def execute_safely(df, code: str):
    SAFE_GLOBALS = {"pd": __import__("pandas")}
    SAFE_LOCALS = {"df": df}

    try:
        exec(code, SAFE_GLOBALS, SAFE_LOCALS)
        return SAFE_LOCALS.get("ANSWER", None)
    except Exception:
        return None
