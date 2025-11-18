from fastapi import APIRouter, UploadFile, File, Form
from app.services.data_loader import load_dataframe
from app.services.schema_service import extract_schema
from app.services.gemini_code_service import generate_processing_code
from app.services.execution_service import execute_safely
from app.services.gemini_nlg_service import generate_summary
from app.services.pdf_service_text import create_pdf
from fastapi.responses import JSONResponse
import base64
from app.services.gemini_validation_service import validate_report_capability
from io import BytesIO

router = APIRouter()


@router.post("/generate")
async def generate_report(
    dataset_type: str = Form(...),
    report_type: str = Form(...),
    output_language: str = Form(...),
    file: UploadFile = File(...)
):
    file_bytes = await file.read()
   
    # Step 1: Load data
    df = load_dataframe(BytesIO(file_bytes), filename=file.filename)

    # Step 2: Extract schema info
    schema_info = extract_schema(df)

    # ⭐ Step 2.5: Validate report capability using Gemini
    validation = validate_report_capability(report_type, df.columns.tolist())

    if not validation["can_generate"]:
        return JSONResponse(
            status_code=400,
            content={
                "error": "Report cannot be generated.",
                "reason": validation["reason"]
            }
        )

    # Step 3: Generate pandas code
    code = generate_processing_code(dataset_type, report_type, schema_info, df.columns)

    # Step 4: Execute user-defined code safely
    result = execute_safely(df, code)

    # Step 5: Generate AI summary
    summary_report = generate_summary(dataset_type, report_type, result, output_language)
    
    pdf_buffer = create_pdf(
        report_title=report_type,
        summary_text=summary_report
    )

    pdf_base64 = base64.b64encode(pdf_buffer.getvalue()).decode("utf-8")

    return JSONResponse({
        "pdf": pdf_base64,
        "summary_text": summary_report
    })


@router.post("/render")
def render_updated_text(payload: dict):
    updated_text = payload["summary_text"]
    title = payload["title"]

    pdf_buffer = create_pdf(
        report_title=title,
        summary_text=updated_text
    )

    pdf_base64 = base64.b64encode(pdf_buffer.getvalue()).decode("utf-8")

    return {"pdf": pdf_base64}

