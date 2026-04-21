import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd  # Thêm dòng này để sửa lỗi 'pd' is not defined

st.set_page_config(
    page_title="Lịch Tập Gym",
    page_icon="🏋️", # Đây sẽ là icon nhỏ trên tab trình duyệt
    layout="wide"
)
# Cấu hình trang
st.set_page_config(page_title="Lịch Tập Gym - Phase 1", layout="wide")

st.title("🏋️ Lộ Trình Tập Luyện Tự Động")
st.markdown("Dữ liệu được kết nối trực tiếp từ Google Sheets của bạn.")

# URL của Google Sheet
sheet_url = "https://docs.google.com/spreadsheets/d/16yke7jWHaKpCDgTph1p29r1JHYpv-qQGQbUsFTNjDa8/edit?usp=sharing"

# Kết nối và đọc dữ liệu
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    # Thêm ttl=600 để cache dữ liệu trong 10 phút, tránh load lại quá nhiều lần
    df = conn.read(spreadsheet=sheet_url, ttl=600)

    # Làm sạch dữ liệu: loại bỏ dòng hoàn toàn trống
    df = df.dropna(subset=['Exercise'])

    # Giao diện lọc dữ liệu ở thanh bên
    st.sidebar.header("Bộ Lọc")

    weeks = df['Week'].unique()
    selected_week = st.sidebar.selectbox("Chọn Tuần:", weeks)

    days = df[df['Week'] == selected_week]['Day'].unique()
    selected_day = st.sidebar.selectbox("Chọn Ngày:", days)

    # Hiển thị tiêu đề ngày tập
    st.subheader(f"📋 Danh sách bài tập: {selected_week} - {selected_day}")

    # Lọc dữ liệu theo lựa chọn
    filtered_df = df[(df['Week'] == selected_week) & (df['Day'] == selected_day)]

    # Hiển thị từng bài tập
    for _, row in filtered_df.iterrows():
        with st.expander(f"🔥 {row['Exercise']}"):
            c1, c2 = st.columns([1, 1])

            with c1:
                st.markdown(f"**🔢 Số hiệp:** {row['Sets']}")
                st.markdown(f"**🔁 Số lần:** {row['Reps']}")
                st.markdown(f"**⏱️ Nghỉ:** {row['Rest']}")
                # Kiểm tra nếu Tempo hoặc Notes có dữ liệu thì mới hiện
                tempo = row['Tempo'] if pd.notna(row['Tempo']) else "Không có"
                st.markdown(f"**⚡ Tempo:** {tempo}")

                if pd.notna(row['Notes']):
                    st.info(f"**Lưu ý:** {row['Notes']}")

            with c2:
                if pd.notna(row['Link']):
                    st.video(row['Link'])
                else:
                    st.warning("Video hướng dẫn đang được cập nhật...")

    # Tùy chọn hiển thị bảng tổng quát
    if st.sidebar.checkbox("Xem bảng dữ liệu chi tiết"):
        st.divider()
        st.dataframe(filtered_df)

except Exception as e:
    st.error(f"Đã xảy ra lỗi khi kết nối: {e}")
    st.info("Mẹo: Hãy đảm bảo file Google Sheet đã được chia sẻ ở chế độ 'Bất kỳ ai có liên kết đều có thể xem'.")