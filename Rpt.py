import streamlit as st
import pandas as pd
import openpyxl as op
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('times', 'fonts/times.ttf'))
import io

def report (TimeF, select_dz, phaF, isc, F79, subs, dis87, dis21, disFL, result_87, result_21, result_FL, dis87_1, dis21_1, disFL_1, result_87_1, result_21_1, result_FL_1):
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    from reportlab.lib.styles import ParagraphStyle

    style = ParagraphStyle(
        name="Vietnamese",
        fontName="Times-Roman",
        fontSize=16,
        leading=24
    )
    content = []

    content.append(Paragraph(f"Thời gian: {TimeF}", style))
    content.append(Paragraph(f"Đường dây sự cố: {select_dz}", style))
    content.append(Paragraph(f"Pha sự cố: {phaF}", style))
    content.append(Paragraph(f"Dòng sự cố Isc: {isc}", style))
    content.append(Paragraph(f"Tình trạng đóng lặp lại: {F79}", style))
    

    data = [
        ("Khoảng cách F87", dis87, result_87),
        ("Khoảng cách F21", dis21, result_21),
        ("Khoảng cách FL", disFL, result_FL),
    ]

    if not any([dis21, dis87, disFL]):
        content.append(Paragraph(f"*{subs[0]} : No data", style))
    else:
        content.append(Paragraph(f"*{subs[0]}", style))

        for label, dis, result in data:
            if dis:
                text = f"     - {label}: {dis}m <=> tương ứng khoảng cột {result[0]}-{result[1]}"
            else:
                text = f"     - {label}: No data"

            content.append(Paragraph(text, style))

    data_1 = [
        ("Khoảng cách F87", dis87_1, result_87_1),
        ("Khoảng cách F21", dis21_1, result_21_1),
        ("Khoảng cách FL", disFL_1, result_FL_1),
    ]

    if not any([dis21_1, dis87_1, disFL_1]):
        content.append(Paragraph(f"*{subs[1]} : No data", style))
    else:
        content.append(Paragraph(f"*{subs[1]}", style))

        for label, dis, result in data_1:
            if dis:
                text = f"     - {label}: {dis}m <=> tương ứng khoảng cột {result[0]}-{result[1]}"
            else:
                text = f"     - {label}: No data"

            content.append(Paragraph(text, style))


    doc.build(content)


    st.download_button(
    label="📥 Download PDF",
    data=buffer,
    file_name="Fault_info.pdf",
    mime="application/pdf",
    width="stretch")
    return None  
