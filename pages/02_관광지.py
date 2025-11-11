import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="서울 관광지도 🌏", page_icon="🗺️")

st.title("🌸 외국인들이 좋아하는 서울 관광지 TOP 10")
st.write("서울을 대표하는 인기 명소들을 지도와 함께 살펴보세요! 🧭")

# 관광지 데이터
places = [
    {
        "name": "경복궁",
        "lat": 37.579617, "lon": 126.977041,
        "desc": "조선시대의 대표 궁궐로, 한국 전통건축의 아름다움을 느낄 수 있는 명소예요.",
        "station": "경복궁역 (3호선)"
    },
    {
        "name": "명동 쇼핑거리",
        "lat": 37.563756, "lon": 126.982669,
        "desc": "서울의 대표 쇼핑거리로, 패션·화장품·길거리음식이 가득해요.",
        "station": "명동역 (4호선)"
    },
    {
        "name": "남산타워 (N서울타워)",
        "lat": 37.551169, "lon": 126.988227,
        "desc": "서울의 전경을 한눈에 볼 수 있는 전망대! 야경이 특히 아름다워요.",
        "station": "명동역 (4호선)"
    },
    {
        "name": "북촌 한옥마을",
        "lat": 37.582604, "lon": 126.983998,
        "desc": "전통 한옥이 모여 있는 아름다운 마을로, 사진 명소로 유명해요.",
        "station": "안국역 (3호선)"
    },
    {
        "name": "동대문디자인플라자 (DDP)",
        "lat": 37.566478, "lon": 127.009204,
        "desc": "현대적인 디자인 랜드마크로, 패션과 전시의 중심지예요.",
        "station": "동대문역사문화공원역 (2·4·5호선)"
    },
    {
        "name": "홍대거리",
        "lat": 37.556332, "lon": 126.922651,
        "desc": "젊음과 예술의 거리! 거리공연과 개성 있는 가게들이 가득해요.",
        "station": "홍대입구역 (2호선)"
    },
    {
        "name": "롯데월드",
        "lat": 37.5110, "lon": 127.0980,
        "desc": "서울 대표 놀이공원으로, 실내외 어트랙션과 쇼핑몰이 함께 있어요.",
        "station": "잠실역 (2·8호선)"
    },
    {
        "name": "청계천",
        "lat": 37.5700, "lon": 126.9910,
        "desc": "도심 속 산책길로, 밤에는 조명이 아름답게 빛나요.",
        "station": "종각역 (1호선)"
    },
    {
        "name": "인사동 문화거리",
        "lat": 37.5740, "lon": 126.9849,
        "desc": "전통과 현대가 어우러진 거리로, 공예품과 찻집이 많아요.",
        "station": "종로3가역 (1·3·5호선)"
    },
    {
        "name": "이태원",
        "lat": 37.5345, "lon": 126.9946,
        "desc": "다양한 외국문화가 공존하는 글로벌 거리예요. 음식 탐방에도 딱이에요!",
        "station": "이태원역 (6호선)"
    },
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

# 지도 표시 (크기 80%)
st_folium(m, width=560, height=400)

# 구분선
st.markdown("---")

# 관광지 소개
st.subheader("🏙️ 관광지 소개 & 지하철역 안내")
for i, p in enumerate(places, start=1):
    st.markdown(f"**{i}. {p['name']}** — {p['desc']} _(가까운 역: {p['station']})_")
