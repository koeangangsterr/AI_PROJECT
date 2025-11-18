import streamlit as st
import csv
from datetime import datetime

st.title("🌫️ 2024년 12월 서울 미세먼지 시간대 분석")
st.write("날짜와 구를 선택하면 시간대별 미세먼지 농도를 분석해 외출하기 좋은 시간을 추천해줘요!")

# 1) CSV 데이터 불러오기 (기본 csv 모듈만 사용)
FILE_PATH = "10115misemeonjiji.csv"

data = []
with open(FILE_PATH, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        data.append(row)

# 2) 날짜 목록 추출
dates = sorted(list(set([row["date"] for row in data])))

# Streamlit UI: 날짜 선택
selected_date = st.selectbox("📅 날짜 선택", dates)

# 3) 해당 날짜의 구 목록 추출
gus = sorted(list(set([row["gu"] for row in data if row["date"] == selected_date])))

selected_gu = st.selectbox("🏙️ 구 선택", gus)

# 4) 선택한 날짜 + 구의 시간대별 미세먼지 데이터 필터링
filtered = [row for row in data if row["date"] == selected_date and row["gu"] == selected_gu]

# 시간대 정렬
filtered = sorted(filtered, key=lambda x: int(x["hour"]))

# 5) 화면에 시간대별 미세먼지 표시
st.subheader(f"📊 {selected_date} / {selected_gu} 시간대별 미세먼지 농도 (㎍/㎥)")

hours = []
values = []

for row in filtered:
    hour = f"{row['hour']}시"
    value = float(row["pm10"])
    hours.append(hour)
    values.append(value)

# 표 출력
for h, v in zip(hours, values):
    st.write(f"- **{h} → {v} ㎍/㎥**")

# 6) 외출하기 좋은 시간 계산
st.subheader("🌤️ 외출하기 좋은 시간대 추천")

# 기준:
#  0–30 좋음
# 31–80 보통
# 81–150 나쁨
# 151+ 매우 나쁨

good_times = []
normal_times = []

for h, v in zip(hours, values):
    if v <= 30:
        good_times.append(h)
    elif v <= 80:
        normal_times.append(h)

if good_times:
    st.success("✨ **가장 좋은 시간대 (PM10 ≤ 30)**")
    st.write(" / ".join(good_times))

if normal_times:
    st.info("🙂 **무난한 시간대 (PM10 31~80)**")
    st.write(" / ".join(normal_times))

if not good_times and not normal_times:
    st.warning("⚠️ 오늘은 미세먼지가 전반적으로 높아요. 외출을 가급적 줄이는 걸 추천해요.")
