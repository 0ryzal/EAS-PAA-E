#!/usr/bin/env python3
"""
build_declaration.py — Generate report/Declaration.pdf (Academic Integrity Pledge).

This produces the signed-declaration template required by EF234405 §5. Each member
must add their signature (handwritten or digital) and fill in their name / Student
ID before the PDF is included in the submission ZIP.

Run:  python report/build_declaration.py
"""

from __future__ import annotations
import os
import matplotlib
from fpdf import FPDF, XPos, YPos

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(matplotlib.get_data_path(), "fonts", "ttf")

# Mirror the team details from build_report.py — EDIT BEFORE SUBMITTING.
MEMBERS = [
    ("Muhammad Rizal Hafiyyan", "5025231212"),
]
CITY_DATE = "Surabaya, 18 June 2026"
CONTRIB = [
    "Muhammad Rizal Hafiyyan — 100%: Design, formal model & architecture; "
    "Dijkstra (core) + MinHeap; Bellman-Ford baseline; A* (bonus); CLI demo & "
    "route visualiser; correctness proof; complexity analysis; benchmark harness, "
    "plots & report.",
]

PLEDGE = (
    "By the name of Allah (God) Almighty, I hereby pledge and declare that I have "
    "completed this Final Exam project as part of my team's independent work. I have "
    "not engaged in cheating, plagiarism, or received unauthorized assistance in any "
    "form. I further declare that any use of AI tools was limited to a supportive role "
    "(such as for grammar checking or debugging) and that the final solution is the "
    "product of my team's own intellectual effort. I understand that I will accept all "
    "consequences if I am found to have violated this academic integrity pledge."
)


def build():
    pdf = FPDF(format="A4")
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.set_margins(22, 20, 22)
    pdf.add_font("DejaVu", "", os.path.join(FONT_DIR, "DejaVuSans.ttf"))
    pdf.add_font("DejaVu", "B", os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf"))
    pdf.add_font("DejaVu", "I", os.path.join(FONT_DIR, "DejaVuSans-Oblique.ttf"))
    pdf.add_page()

    pdf.set_font("DejaVu", "B", 13)
    pdf.set_text_color(20, 50, 110)
    pdf.multi_cell(0, 8, "EF234405 — Design & Analysis of Algorithms",
                   align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.multi_cell(0, 8, "Final Exam — Academic Integrity Pledge (Declaration)",
                   align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_text_color(0)
    pdf.ln(6)

    pdf.set_font("DejaVu", "B", 11)
    pdf.multi_cell(0, 7, "Project: SIGAP — Fastest-Route Emergency Dispatch on City "
                   "Road Networks", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(4)

    pdf.set_font("DejaVu", "I", 11)
    pdf.set_fill_color(245, 245, 248)
    pdf.multi_cell(0, 6.5, "“" + PLEDGE + "”", border=1, fill=True,
                   new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(8)

    pdf.set_font("DejaVu", "", 11)
    pdf.multi_cell(0, 7, CITY_DATE, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(12)

    # Signature blocks
    pdf.set_font("DejaVu", "", 11)
    for name, sid in MEMBERS:
        pdf.cell(0, 7, "_______________________________",
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font("DejaVu", "B", 11)
        pdf.cell(0, 6, name, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font("DejaVu", "", 11)
        pdf.cell(0, 6, f"Student ID: {sid}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(10)

    pdf.ln(2)
    pdf.set_font("DejaVu", "B", 11)
    pdf.multi_cell(0, 7, "Contribution declaration",
                   new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("DejaVu", "", 10.5)
    for c in CONTRIB:
        x = pdf.get_x()
        pdf.cell(5, 6, "•")
        pdf.set_x(x + 5)
        pdf.multi_cell(0, 6, c, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    out = os.path.join(HERE, "Declaration.pdf")
    pdf.output(out)
    print(f"Wrote {out}")


if __name__ == "__main__":
    build()
