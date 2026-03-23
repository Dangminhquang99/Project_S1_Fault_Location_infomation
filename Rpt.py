import streamlit as st
import pandas as pd
import openpyxl as op
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('times', 'times.ttf'))
import io

def report (TimeF, phaF, F79, select_dz, subs, dis87, dis21, result_87, result_21, dis87_1, dis21_1, result_87_1, result_21_1):
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    from reportlab.lib.styles import ParagraphStyle

    style = ParagraphStyle(
        name="Vietnamese",
        fontName="times",
        fontSize=12
    )
    content = []

    content.append(Paragraph(f"Thời gian: {TimeF}", style))
    content.append(Paragraph(f"Đường dây sự cố: {select_dz}", style))
    content.append(Paragraph(f"Pha sự cố: {phaF}", style))
    content.append(Paragraph(f"Tình trạng đóng lặp lại: {F79}", style))
    if not dis21 and not dis87:
        content.append(Paragraph(f"***{subs[0]} :No data", style))
    else:
        content.append(Paragraph(f"{subs[0]}", style))
        if dis87:
            content.append(Paragraph(f"     - Khoảng cách F87: {dis87}m <=> tương ứng khoảng cột {result_87[0]}-{result_87[1]}", style))
        else:
            content.append(Paragraph(f"     - Khoảng cách F87: No data", style))
        if dis21:
            content.append(Paragraph(f"     - Khoảng cách F21: {dis21}m <=> tương ứng khoảng cột {result_21[0]}-{result_21[1]}", style))
        else:
            content.append(Paragraph(f"     - Khoảng cách F21: No data", style))

    if not dis21_1 and not dis87_1:
        content.append(Paragraph(f"{subs[1]} :No data", style))
    else:
        content.append(Paragraph(f"***{subs[1]}", style))
        if dis87_1:
            content.append(Paragraph(f"     - Khoảng cách F87: {dis87_1}m <=> tương ứng khoảng cột {result_87_1[0]}-{result_87_1[1]}", style))
        else:
            content.append(Paragraph(f"     - Khoảng cách F87: No data", style))
        if dis21_1:
            content.append(Paragraph(f"     - Khoảng cách F21: {dis21_1}m <=> tương ứng khoảng cột {result_21_1[0]}-{result_21_1[1]}", style))
        else:
            content.append(Paragraph(f"     - Khoảng cách F21: No data", style))
    doc.build(content)


    st.download_button(
    label="📥 Download PDF",
    data=buffer,
    file_name="sum_report.pdf",
    mime="application/pdf")
    return None   
