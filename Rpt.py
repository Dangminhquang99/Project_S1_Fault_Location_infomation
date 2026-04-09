import streamlit as st
import pandas as pd
import openpyxl as op
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('times', 'fonts/times.ttf'))
pdfmetrics.registerFont(TTFont('times-italic', 'fonts/timesi.ttf'))
pdfmetrics.registerFont(TTFont('times-bold', 'fonts/timesbd.ttf'))
import io

pdfmetrics.registerFontFamily(
    'times',
    normal='times',
    bold='times-bold',
    italic='times-italic',
    boldItalic='times-bolditalic'
)


def report (TimeF, select_dz, phaF, isc, weather, F79, subs, dis87, dis21, disFL, result_87, result_21, result_FL, dis87_1, dis21_1, disFL_1, result_87_1, result_21_1, result_FL_1, TQLVH, comment):
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    from reportlab.lib.styles import ParagraphStyle

    style = ParagraphStyle(
        name="Vietnamese",
        fontName="Times",
        fontSize=14,
        leading=20
    )
    style_1 = ParagraphStyle(
        name="Vietnamese",
        fontName="Times",
        fontSize=12,
        leading=16
    )
    content = []
    content.append(Paragraph(f" ----------------------  <b>THÔNG TIN SỰ CỐ ĐƯỜNG DÂY</b>  ----------------------<br/>", style))
    content.append(Paragraph(f"Thời gian: {TimeF}", style))
    content.append(Paragraph(f"Đường dây sự cố: {select_dz}", style))
    content.append(Paragraph(f"Pha sự cố: {phaF}", style))
    content.append(Paragraph(f"Dòng sự cố Isc: {isc} (A)", style))
    content.append(Paragraph(f"Tình trạng đóng lặp lại: {F79}", style))
    content.append(Paragraph(f"Thời tiết: {weather}", style))
    

    data = [
        ("Khoảng cách F87", dis87, result_87),
        ("Khoảng cách F21", dis21, result_21),
        ("Khoảng cách FL", disFL, result_FL),
    ]

    if not any([dis21, dis87, disFL]):
        content.append(Paragraph(f"*<b>{subs[0]} : No data</b>", style))
    else:
        content.append(Paragraph(f"<b>*{subs[0]}</b>", style))

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
        content.append(Paragraph(f"<b>*{subs[1]} : No data</b>", style))
    else:
        content.append(Paragraph(f"<b>*{subs[1]}</b>", style))

        for label, dis, result in data_1:
            if dis:
                text = f"     - {label}: {dis}m <=> tương ứng khoảng cột {result[0]}-{result[1]}"
            else:
                text = f"     - {label}: No data"

            content.append(Paragraph(text, style))
   
    content.append(Paragraph(f"<br/><b>Ghi chú:</b> <i>{comment}</i>", style_1))
    content.append(Paragraph(f"<br/><br/><br/>", style))


    if TQLVH=="Tổ QLVH đường dây Nha Trang":
        content.append(Paragraph(f"Đơn vị QLVH:<br/>* <i>Tổ QLVH DZ Nha Trang, SĐT: 0888007911, Email: TQLVHDZNhaTrang</i>", style_1))
    elif TQLVH=="Tổ QLVH đường dây Cam Ranh":
        content.append(Paragraph(f"Đơn vị QLVH:<br/>* <i>Tổ QLVH DZ Cam Ranh, SĐT: 0839861405, Email: TQLVHDZCamRanh</i>", style_1))    
    elif TQLVH=="Tổ QLVH đường dây Phan Rang":
        content.append(Paragraph(f"Đơn vị QLVH:<br/>* <i>Tổ QLVH DZ Phan Rang, SĐT: 0866236556, Email:  toqlvhdzphanrang@gmail.com </i>", style_1)) 
    elif TQLVH=="Tổ QLVH đường dây Cam Ranh, Phan Rang":
        content.append(Paragraph(f"Đơn vị QLVH:<br/>* <i>Tổ QLVH DZ Cam Ranh, SĐT: 0839861405, Email: TQLVHDZCamRanh<br/>* Tổ QLVH DZ Phan Rang, SĐT: 0866236556, Email:  toqlvhdzphanrang@gmail.com </i>", style_1))
    elif TQLVH =="Tổ QLVH đường dây Nha Trang, Cam Ranh, Phan Rang":
        content.append(Paragraph(f"Đơn vị QLVH:<br/>* <i>Tổ QLVH DZ Nha Trang, SĐT: 0888007911, Email: TQLVHDZNhaTrang<br/>* Tổ QLVH DZ Cam Ranh, SĐT: 0839861405, Email: TQLVHDZCamRanh<br/>* Tổ QLVH DZ Phan Rang, SĐT: 0866236556, Email:  toqlvhdzphanrang@gmail.com </i>", style_1))

    doc.build(content)


    st.download_button(
    label="📥 Download PDF",
    data=buffer,
    file_name="Fault_info.pdf",
    mime="application/pdf",
    width="stretch")
    return None
