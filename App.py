import streamlit as st
import pandas as pd
import openpyxl as op
import Gfile as gf
import Algo as al
import Rpt as rbt

# Cài đặt định dạng trang web
st.set_page_config(page_title="Tra cứu sự cố",layout="wide",initial_sidebar_state="expanded")

# Cài đặt tittle và chế độ chia cột
colm1, colm2=st.columns([5,1],vertical_alignment="bottom")
colm1.title("📊 TRA CỨU SỰ CỐ" )
view_mode=colm2.toggle("🔄 Chế độ chia cột")

# Lựa chọn tình trạng đóng lặp lại
F79, TimeF, select_dz, phaF = al.initial_info()

#Cấu hình đường dây, tba
#select_dz=gf.select_name_dz()
subs=gf.select_tba_1(select_dz)
df = gf.accum(select_dz)

#Chạy chương trình
colm6, colm7=st.columns(2)
if view_mode:
    with colm6:  #TẠI TBA 1 #cột 1
            al.process(subs[0],df,"subs_0")
    with colm7:#TẠI TBA 2 #cột 2
            al.process(subs[1],df,"subs_1")
else:   
    #with st.expander(f"{subs[0]}"): #TẠI TBA 1 #cột 1
        dis87, dis21, result_87, result_21 = al.process(subs[0], df,"subs_0")
   # with st.expander(f"{subs[1]}"): #TẠI TBA 2 #cột 2
        dis87_1, dis21_1, result_87_1, result_21_1=al.process(subs[1], df,"subs_1")

rbt.report(TimeF, phaF, F79, select_dz, subs, dis87, dis21, result_87, result_21, dis87_1, dis21_1, result_87_1, result_21_1)
