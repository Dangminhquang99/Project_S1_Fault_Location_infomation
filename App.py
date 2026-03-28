import streamlit as st
import pandas as pd
import openpyxl as op
import Gfile as gf
import Algo as al
import Rpt as rbt

# Cài đặt định dạng trang web
st.set_page_config(page_title="Tra cứu sự cố",layout="wide",initial_sidebar_state="expanded")

st.title("⚡ TRA CỨU SỰ CỐ" )

# Thông tin ban đầu
TimeF, select_dz, phaF, F79, isc, dis87, dis21, disFL, dis87N1, dis21N1, disFLN1,subs, df = al.initial_info()

#Khởi chạy tiến trình tại trạm biến áp 1
dis87, dis21, disFL, result_87, result_21, result_FL, value87,value21, valueFL = al.process(subs[0], df,"subs_0",dis87, dis21, disFL)

    #Khởi chạy tiến trình tại trạm biến áp 2
dis87_1, dis21_1, disFL_1, result_87_1, result_21_1, result_FL_1, value87_1,value21_1, valueFL_1 = al.process(subs[1], df,"subs_1", dis87N1, dis21N1, disFLN1)

search=st.button("🔍 Tra cứu", key=f"{subs}",type="primary",width="stretch")
if search:
    if result_87:
        al.info(df, result_87, "F87", value87, subs[0])

    if result_21:
        al.info(df, result_21, "F21", value21, subs[0])

    if result_FL:
        al.info(df, result_FL, "FL", valueFL, subs[0])

    if result_87_1:
        al.info(df, result_87_1, "F87", value87_1, subs[1])

    if result_21_1:
        al.info(df, result_21_1, "F21", value21_1, subs[1])

    if result_FL_1:
        al.info(df, result_FL_1, "FL", valueFL_1, subs[1])



rbt.report(TimeF, select_dz, phaF, isc, F79, subs, dis87, dis21, disFL, result_87, result_21, result_FL, dis87_1, dis21_1, disFL_1, result_87_1, result_21_1, result_FL_1)
