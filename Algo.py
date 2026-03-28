import streamlit as st
import pandas as pd
import Gfile as gf

def initial_info():
    tendz_map=gf.tendz_map
    TimeF=st.text_input("⏰ Thời gian sự cố",placeholder="00:00:00 ngày 01/01/2025")
    select_dz=gf.select_name_dz(tendz_map)
    subs=gf.select_tba_1(select_dz)
    df = gf.accum(select_dz)
    phaF = st.pills("Pha sự cố:", ["A-B-C","A-N", "B-N", "C-N", "AB", "BC", "AC"])
    F79 = st.pills("Tình trạng đóng lặp lại:", ["Thành công", "Không thành công", "Không đóng lặp lại"])
    isc= st.number_input(f"Dòng sự cố:", min_value=0)

    st.subheader(f"📍{subs[0]}")
    colm1, colm2, colm3=st.columns(3)
    with colm1: dis87 = st.number_input(f"📏 Nhập khoảng cách sự cố F87/{subs[0]}:", min_value=0,step=500)
    with colm2: dis21 = st.number_input(f"📏 Nhập khoảng cách sự cố F21/{subs[0]}:", min_value=0,step=500)
    with colm3: disFL = st.number_input(f"📏 Nhập khoảng cách sự cố FL/{subs[0]}:", min_value=0,step=500)


    st.subheader(f"📍{subs[1]}")
    colm4, colm5, colm6=st.columns(3)
    with colm4: dis87N1 = st.number_input(f"📏 Nhập khoảng cách sự cố F87/{subs[1]}:", min_value=0,step=500)
    with colm5: dis21N1 = st.number_input(f"📏 Nhập khoảng cách sự cố F21/{subs[1]}:", min_value=0,step=500)
    with colm6: disFLN1 = st.number_input(f"📏 Nhập khoảng cách sự cố FL/{subs[1]}:", min_value=0,step=500)
    st.write(f" 📡***Tổng chiều dài đường dây: {df['Chiều dài'].sum()} m***")

    return TimeF, select_dz, phaF, F79, isc, dis87, dis21, disFL, dis87N1, dis21N1, disFLN1,subs, df




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
    return result, value    
                

def info(df, result, role_name, value, subs):
    if value:
        if not result:
            st.warning(f"⚠️ Không tìm thấy khoảng phù hợp với giá trị đã nhập, hãy đảm bảo rằng giá trị nằm trong phạm vi chiều dài của đường dây! ")
        elif len(result)==2:
            st.info(f"🔍 Khoảng cách rơ le {role_name}/{subs} tương đương khoảng cột {result[0]} - {result[1]}.")
        elif len(result)==3:
            st.info(f"🔍 Khoảng cách rơ le {role_name}/{subs} tương đương khoảng cột {result[0]} - {result[1]} - {result[2]}.")          

    if not result:
        st.warning(f"⚠️ Không có dữ liệu kết quả để hiển thị cho {role_name}.")
        return
    if 'Vị trí' not in df.columns:
        st.error("❌ File thông tin cột thiếu cột 'Vị trí'.")
        return
    get_col=df.query("`Vị trí` in @result")[['Vị trí','Khoảng cột', 'Công dụng cột','Thứ tự pha','Chiều dài']]
    st.write(get_col.T)

    #Định vị trên bản đồ
    lat=df.query("`Vị trí` in @result")['Latitude']
    lon=df.query("`Vị trí` in @result")['Longitude']
    maps_url_0 = f"https://www.google.com/maps?q={lat.iloc[0]},{lon.iloc[0]}"
    st.markdown(f"[🗺️ Xem trên bản đồ: VT {result[0]}]({maps_url_0})", unsafe_allow_html=True)
    maps_url_1 = f"https://www.google.com/maps?q={lat.iloc[1]},{lon.iloc[1]}"
    st.markdown(f"[🗺️ Xem trên bản đồ: VT {result[1]}]({maps_url_1})", unsafe_allow_html=True)


def process(subs, df, subs_no, dis87, dis21, disFL):

    result_87, value87 = find_positions(dis87, df, "F87", subs_no)
    result_21, value21 = find_positions(dis21, df, "F21", subs_no)
    result_FL, valueFL = find_positions(disFL, df, "FL", subs_no)

    return dis87, dis21, disFL, result_87, result_21, result_FL, value87,value21, valueFL
    

