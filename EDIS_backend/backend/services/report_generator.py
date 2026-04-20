from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch


def generate_pdf_bytes(data: dict) -> bytes:
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    # Title
    story.append(Paragraph("<b>EDIS Ecosystem Report</b>", styles["Title"]))
    story.append(Spacer(1, 0.3 * inch))

    # Summary
    story.append(Paragraph(f"Status: {data['status']}", styles["Normal"]))
    story.append(
        Paragraph(
            f"Ecosystem Stress Index: {data['ecosystem_stress_index']}",
            styles["Normal"],
        )
    )
    story.append(
        Paragraph(
            f"Resilience Index: {data['resilience_index']}",
            styles["Normal"],
        )
    )
    story.append(Spacer(1, 0.4 * inch))

    # Components section
    story.append(Paragraph("<b>Component Breakdown</b>", styles["Heading2"]))
    story.append(Spacer(1, 0.2 * inch))

    for k, v in data["components"].items():
        story.append(
            Paragraph(f"{k.capitalize()}: {v:.2f}", styles["Normal"])
        )
        story.append(Spacer(1, 0.2 * inch))

    doc.build(story)

    buffer.seek(0)
    return buffer.getvalue()
