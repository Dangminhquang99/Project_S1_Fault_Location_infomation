import streamlit as st
import pandas as pd
import Gfile as gf

def initial_info():
    tendz_map=gf.tendz_map
    TimeF=st.text_input("🔢 Thời gian sự cố",placeholder="00:00:00 ngày 01/01/2025")
    select_dz=gf.select_name_dz(tendz_map)
    PhaF = st.pills("Pha sự cố:", ["A-N", "B-N", "C-N", "AB", "BC", "AC"])
    F79 = st.pills("Tình trạng đóng lặp lại:", ["Thành công", "Không thành công", "Không đóng lặp lại"])
    return F79, TimeF, select_dz, PhaF

def find_positions(value, data,role_name,subs_no):
    lower=0     #Khoi tao lower bang 0
    result=None #Khoi tao result bang None nham tranh gop loi

    if 'Chiều dài' not in data.columns or data.empty:
        st.error(f"❌ Dữ liệu không hợp lệ hoặc thiếu cột 'Chiều dài'")
        return None
    if subs_no=="subs_0":
        for i in range(len(data)-1):
            lower=data['Chiều dài'].iloc[i]+lower
            upper=lower+data['Chiều dài'].iloc[i+1]
            if value==lower:        #Neu value bang lower
                result = data['Vị trí'].iloc[i-1],data['Vị trí'].iloc[i], data['Vị trí'].iloc[i + 1]  
            elif min(lower, upper) < value <= max(lower, upper):
                result = data['Vị trí'].iloc[i], data['Vị trí'].iloc[i + 1]

    if subs_no=="subs_1":           #TBA so 1
        for i in range(len(data)-1,-1,-1):
            lower=data['Chiều dài'].iloc[i]+lower
            upper=lower+data['Chiều dài'].iloc[i-1]
            if value==lower and i!=len(data)-1:
                result = data['Vị trí'].iloc[i-1],data['Vị trí'].iloc[i], data['Vị trí'].iloc[i + 1]   
            elif min(lower, upper) < value <= max(lower, upper):
                result = data['Vị trí'].iloc[i - 1],data['Vị trí'].iloc[i]
        
                
    if value:
        if not result:
            st.warning(f"⚠️ Không tìm thấy khoảng phù hợp với giá trị đã nhập, hãy đảm bảo rằng giá trị nằm trong phạm vi chiều dài của đường dây! ")
        elif len(result)==2:
            st.info(f"🔍 Khoảng cách rơ le {role_name} tương đương khoảng cột {result[0]} - {result[1]}.")
        elif len(result)==3:
            st.info(f"🔍 Khoảng cách rơ le {role_name} tương đương khoảng cột {result[0]} - {result[1]} - {result[2]}.")          
        return result
    return None


def info(df, result, role_name):
    if not result:
        st.warning(f"⚠️ Không có dữ liệu kết quả để hiển thị cho {role_name}.")
        return
    if 'Vị trí' not in df.columns:
        st.error("❌ File thông tin cột thiếu cột 'Vị trí'.")
        return
    get_col=df.query("`Vị trí` in @result")[['Vị trí','Khoảng cột', 'Công dụng cột','Thứ tự pha','Chiều dài']]
    st.write(get_col.T)


def process(subs, df, subs_no):
    st.header(f"📋{subs}")
    st.write(f" 🔍***Tổng chiều dài đường dây: {df['Chiều dài'].sum()} m***")
    st.markdown("---")
    dis87 = st.number_input(f"🔢 Nhập khoảng cách sự cố F87/{subs}:", min_value=0,step=500)
    dis21 = st.number_input(f"🔢 Nhập khoảng cách sự cố F21/{subs}:", min_value=0,step=500)
    result_87 = find_positions(dis87, df, "F87", subs_no)
    if result_87:
        info(df, result_87, "F87")
        directions (df, result_87)
    result_21 = find_positions(dis21, df, "F21", subs_no)
    if result_21:
        info(df, result_21, "F21")
        directions (df, result_21)
    return dis87, dis21, result_87, result_21


 
def directions (df, result):
    if result:
        lat=df.query("`Vị trí` in @result")['Latitude']
        lon=df.query("`Vị trí` in @result")['Longitude']
        maps_url_0 = f"https://www.google.com/maps?q={lat.iloc[0]},{lon.iloc[0]}"
        st.markdown(f"[🗺️ Xem trên bản đồ: VT {result[0]}]({maps_url_0})", unsafe_allow_html=True)
        maps_url_1 = f"https://www.google.com/maps?q={lat.iloc[1]},{lon.iloc[1]}"
        st.markdown(f"[🗺️ Xem trên bản đồ: VT {result[1]}]({maps_url_1})", unsafe_allow_html=True)
    return None
    

