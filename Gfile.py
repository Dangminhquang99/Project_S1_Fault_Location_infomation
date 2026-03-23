import streamlit as st
import pandas as pd
import openpyxl as op



g_map=pd.read_excel("data/mapping.xlsx")                                                    #doc file mapping
tendz_map = pd.Series(g_map['TEN FILE'].values, index=g_map['TEN DZ']).to_dict()            #Anh xa ten duong day -> ten file
tba_map = pd.Series(zip(g_map['TBA1'], g_map['TBA2']), index=g_map['TEN DZ']).to_dict()     #Anh xa ten duong day -> ten TBA 1, TBA2

def select_name_dz(tendz_map):
    select_dz = st.selectbox("📂 Hãy chọn đường dây", list(tendz_map.keys()),index=None,placeholder="Chọn 01 đường dây trong danh sách") or st.stop()
    return select_dz

def select_tba_1(select_dz):
    select_tba = tba_map.get(select_dz,[])
    return select_tba

def accum(select_dz):
    excel_name= tendz_map.get(select_dz,None)
    if not excel_name:
        st.error("❌ Không tìm thấy ánh xạ đúng cho đường dây đã chọn.")
        return None
    path_excel = f"data/{excel_name}"
    try:
        df = pd.read_excel(path_excel)
    except Exception as e:
        st.error(f"❌ Lỗi khi đọc file: {e}")
        return pd.DataFrame()
    return df
