import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="서울 관광지도 🌏", page_icon="🗺️")

st.title("🌸 외국인들이 좋아하는 서울 관광지 TOP 10")
st.write("서울의 인기 명소를 폴리움 지도 위에 표시했어요! 클릭하면 이름을 볼 수 있어요 😄")

# 관광지 데이터
places = [
    {"name": "경복궁", "lat": 37.579617, "lon": 126.977041},
    {"name": "명동 쇼핑거리", "lat": 37.563756, "lon": 126.982669},
    {"name": "남산타워 (N서울타워)", "lat": 37.551169, "lon": 126.988227},
    {"name": "북촌 한옥마을", "lat": 37.582604, "lon": 126.983998},
    {"name": "동대문디자인플라자 (DDP)", "lat": 37.566478, "lon": 127.009204},
    {"name": "홍대거리", "lat": 37.556332, "lon": 126.922651},
    {"name": "롯데월드", "lat": 37.5110, "lon": 127.0980},
    {"name": "청계천", "lat": 37.5700, "lon": 126.9910},
    {"name": "인사동 문화거리", "lat": 37.5740, "lon": 126.9849},
    {"name": "이태원", "lat": 37.5345, "lon": 126.9946},
]

# 지도 생성
m = folium.Map(location=[37.5665, 126.9780], zoom_start=12)

# 마커 추가
for p in places:
    folium.Marker(
        location=[p["lat"], p["lon"]],
        popup=p["name"],
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)

# 지도 표시
st_folium(m, width=700, height=500)
