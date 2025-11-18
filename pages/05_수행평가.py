import streamlit as st
import csv
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(CURRENT_DIR, "..", "10115misemeonjiji.csv")

st.title("CSV 컬럼 구조 확인용")

def load_csv(path):
    encodings = ["utf-8", "utf-8-sig", "cp949", "euc-kr"]
    for enc in encodings:
        try:
            with open(path, "r", encoding=enc) as f:
                reader = csv.reader(f)
                headers = next(reader)  # 첫 줄 읽기
                st.write("📌 **CSV 헤더:**")
                st.write(headers)
                return
        except Exception as e:
            pass

    st.error("CSV 파일을 어떤 인코딩으로도 읽을 수 없습니다.")
    return

load_csv(FILE_PATH)

import streamlit as st
import csv
import os

st.title("🌫️ 2024년 12월 서울 미세먼지 시간대 분석")
st.write("날짜와 구를 선택하면 시간대별 미세먼지 농도를 분석하여 외출하기 좋은 시간을 추천합니다.")

# CSV 위치 자동 인식
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(CURRENT_DIR, "..", "10115misemeonjiji.csv")

# 여러 인코딩 자동 시도
def load_csv(path):
    encodings = ["utf-8", "utf-8-sig", "cp949", "euc-kr"]
    for enc in encodings:
        try:
            with open(path, "r", encoding=enc) as f:
                reader = csv.DictReader(f)
                return list(reader)
        except Exception:
            pass
    return None

data = load_csv(FILE_PATH)

if data is None:
    st.error(f"""
❌ CSV 파일을 읽지 못했습니다.

가능한 원인:
- 파일이 UTF-8/CP949/EUC-KR 인코딩이 아님
- 파일 이름이 다름
- 파일이 프로젝트 최상위 폴더에 없음

CSV 파일을 아래 위치에 놓아주세요:
`/ai_project/10115misemeonjiji.csv`
    """)
    st.stop()

# 날짜 목록
dates = sorted(list(set([row["date"] for row in data])))
selected_date = st.selectbox("📅 날짜 선택", dates)

# 구 목록
gus = sorted(list(set([row["gu"] for row in data if row["date"] == selected_date])))
selected_gu = st.selectbox("🏙️ 구 선택", gus)

# 데이터 필터링
filtered = [row for row in data if row["date"] == selected_date and row["gu"] == selected_gu]
filtered = sorted(filtered, key=lambda x: int(x["hour"]))

# 출력
st.subheader(f"📊 {selected_date} / {selected_gu} 시간대별 미세먼지 농도")

hours = []
values = []

for row in filtered:
    hour = f"{row['hour']}시"
    value = float(row["pm10"])
    hours.append(hour)
    values.append(value)
    st.write(f"- **{hour:**} {value}㎍/㎥**")

# 추천 로직
st.subheader("🌤️ 외출하기 좋은 시간대 추천")

good = [h for h, v in zip(hours, values) if v <= 30]
normal = [h for h, v in zip(hours, values) if 31 <= v <= 80]

if good:
    st.success("✨ **좋은 시간대 (0~30㎍/㎥)**\n" + ", ".join(good))
if normal:
    st.info("🙂 **무난한 시간대 (31~80㎍/㎥)**\n" + ", ".join(normal))
if not good and not normal:
    st.warning("⚠️ 오늘은 미세먼지가 전반적으로 높습니다. 외출을 줄이는 것을 권장합니다.")
