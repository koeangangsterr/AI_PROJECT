import streamlit as st
import csv
import os

st.title("🌫️ 2024년 12월 서울 미세먼지 시간대 분석")
st.write("날짜와 구를 선택하면 시간대별 미세먼지 농도를 분석해 외출하기 좋은 시간을 추천해줘요!")

# (1) 현재 파일 기준 절대경로 자동 계산
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(CURRENT_DIR, "..", "10115misemeonjiji.csv")

# (2) CSV 로드
data = []
try:
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
except FileNotFoundError:
    st.error("❌ CSV 파일을 찾을 수 없습니다.\n파일을 프로젝트 최상위 폴더에 넣어주세요.")
    st.stop()

# (3) 날짜와 구 선택
dates = sorted(list(set([row["date"] for row in data])))
selected_date = st.selectbox("📅 날짜 선택", dates)

gus = sorted(list(set([row["gu"] for row in data if row["date"] == selected_date])))
selected_gu = st.selectbox("🏙️ 구 선택", gus)

# (4) 시간대별 데이터 필터링
filtered = [row for row in data if row["date"] == selected_date and row["gu"] == selected_gu]
filtered = sorted(filtered, key=lambda x: int(x["hour"]))

# (5) 시간대별 값 출력
st.subheader(f"📊 {selected_date} / {selected_gu} 시간대별 미세먼지 농도")

hours = []
values = []

for row in filtered:
    hour = f"{row['hour']}시"
    value = float(row["pm10"])
    hours.append(hour)
    values.append(value)
    st.write(f"- **{hour}: {value}㎍/㎥**")

# (6) 외출 추천 시간대
st.subheader("🌤️ 외출하기 좋은 시간대 추천")

good = [h for h, v in zip(hours, values) if v <= 30]
normal = [h for h, v in zip(hours, values) if 31 <= v <= 80]

if good:
    st.success("✨ **좋은 시간대 (0~30㎍/㎥)**\n" + ", ".join(good))
if normal:
    st.info("🙂 **무난한 시간대 (31~80㎍/㎥)**\n" + ", ".join(normal))
if not good and not normal:
    st.warning("⚠️ 오늘은 미세먼지가 전반적으로 높습니다. 외출을 줄이는 것이 좋습니다.")
