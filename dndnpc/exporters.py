import json

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    REPORTLAB = True
except Exception:
    REPORTLAB = False

from .generator import format_profile

def export_json(path, npcs):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(npcs, f, ensure_ascii=False, indent=2)

def export_pdf(path, npcs):
    if not REPORTLAB:
        raise RuntimeError("ReportLab není nainstalovaný. Použij: pip install reportlab")

    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4
    y = height - 50

    for npc in npcs:
        lines = format_profile(npc).splitlines()
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, npc.get("name", "NPC").encode("latin-1", "replace").decode("latin-1")[:80])
        y -= 24
        c.setFont("Helvetica", 9)
        for line in lines[2:]:
            if y < 60:
                c.showPage()
                y = height - 50
                c.setFont("Helvetica", 9)
            clean = line.encode("latin-1", "replace").decode("latin-1")
            c.drawString(50, y, clean[:115])
            y -= 12
        y -= 18
        if y < 90:
            c.showPage()
            y = height - 50
    c.save()
