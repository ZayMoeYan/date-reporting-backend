import io
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

def create_pdf(report_title: str, summary_text: str, chart_path: str | None = None):
    buffer = io.BytesIO()  # create PDF in memory

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40,
        title=report_title
    )

    styles = getSampleStyleSheet()
    story = []

    # Title
    title_style = styles['Heading1']
    title_style.fontSize = 22
    title_style.leading = 26
    story.append(Paragraph(report_title, title_style))
    story.append(Spacer(1, 20))

    # Summary
    body_style = styles['BodyText']
    body_style.fontSize = 11
    body_style.leading = 16

    for paragraph in summary_text.split("\n"):
        if paragraph.strip():
            story.append(Paragraph(paragraph, body_style))
            story.append(Spacer(1, 12))

    # Optional chart
    if chart_path:
        img = Image(chart_path, width=150 * mm, preserveAspectRatio=True)
        story.append(img)

    doc.build(story)

    buffer.seek(0)  # rewind buffer for reading
    return buffer  # return PDF BYTES, not a file path
