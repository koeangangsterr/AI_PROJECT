# pages/05_수행평가.py
import streamlit as st
import csv
import os
import re
from statistics import mean
from datetime import datetime

st.set_page_config(page_title="2024-12 서울 미세먼지(시간별)", layout="wide")
st.title("🌫️ 2024년 12월 서울 미세먼지 — 시간대별 분석 & 외출 추천")

# 1) CSV 파일 경로 자동 탐색 (pages/ 안에서 실행될 때를 고려)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
POSSIBLE_PATHS = [
    os.path.join(CURRENT_DIR, "..", "10115misemeonjiji.csv"),
    os.path.join(CURRENT_DIR, "..", "data", "10115misemeonjiji.csv"),
    os.path.join(CURRENT_DIR, "10115misemeonjiji.csv"),
    os.path.join("/", "mnt", "data", "10115misemeonjiji.csv"),
]

FILE_PATH = None
for p in POSSIBLE_PATHS:
    if os.path.exists(p):
        FILE_PATH = p
        break

if FILE_PATH is None:
    st.error("CSV 파일을 찾을 수 없습니다. 프로젝트 최상위 폴더에 `10115misemeonjiji.csv` 파일을 올려주세요.")
    st.stop()

# 2) 여러 인코딩 시도해서 CSV 로드
def try_load(path):
    encodings = ["utf-8", "utf-8-sig", "cp949", "euc-kr"]
    for enc in encodings:
        try:
            with open(path, "r", encoding=enc) as f:
                reader = csv.reader(f)
                rows = list(reader)
                if not rows:
                    continue
                header = rows[0]
                data_rows = rows[1:]
                return header, data_rows, enc
        except Exception:
            continue
    return None, None, None

header, rows, used_enc = try_load(FILE_PATH)
if header is None:
    st.error("CSV를 어떤 인코딩으로도 읽을 수 없습니다. 파일 인코딩을 확인하세요.")
    st.stop()

st.info(f"읽은 파일: `{FILE_PATH}` (인코딩 시도: {used_enc})")
st.write("### 🔎 CSV 헤더 (첫 줄)")
st.write(header)

# 3) 자동 컬럼 매핑 (여러 변형 허용)
def pick_header(headers, candidates):
    low = [h.lower() for h in headers]
    for c in candidates:
        for i, h in enumerate(low):
            if c in h:
                return headers[i]
    return None

date_candidates = ["date", "날짜", "측정일", "측정일시", "day", "date_time", "측정일자"]
gu_candidates = ["gu", "구", "지역", "area", "district", "region", "borough"]
hour_candidates = ["hour", "시간", "time", "시", "시간대"]
pm10_candidates = ["pm10", "미세먼지", "pm_10", "pm10(㎍/㎥)","pm10(㎍/m3)","pm"]

date_col = pick_header(header, date_candidates)
gu_col = pick_header(header, gu_candidates)
hour_col = pick_header(header, hour_candidates)
pm10_col = pick_header(header, pm10_candidates)

st.write("### 🔄 자동 매핑 결과")
st.write({
    "date_col (날짜)": date_col,
    "gu_col (구/지역)": gu_col,
    "hour_col (시간)": hour_col,
    "pm10_col (미세먼지)": pm10_col
})

st.write("만약 위 자동 매핑이 잘못되었다면, 아래에서 직접 컬럼을 지정하세요.")
# 4) 사용자가 직접 선택할 수 있도록 드롭다운 제공 (자동 선택을 기본값으로)
date_col = st.selectbox("날짜 컬럼 선택", header, index=header.index(date_col) if date_col in header else 0)
gu_col = st.selectbox("구(지역) 컬럼 선택", header, index=header.index(gu_col) if gu_col in header else 1 if len(header)>1 else 0)
hour_col = st.selectbox("시간(시간대) 컬럼 선택", header, index=header.index(hour_col) if hour_col in header else 2 if len(header)>2 else 0)
pm10_col = st.selectbox("미세먼지(PM10) 컬럼 선택", header, index=header.index(pm10_col) if pm10_col in header else 3 if len(header)>3 else 0)

# 5) helper: 숫자 정리 함수
def to_float_safe(s):
    if s is None:
        return None
    s = str(s).strip()
    if s == "":
        return None
    # 제거: 단위, 공백, 쉼표
    s = s.replace(",", "")
    s = re.sub(r"[^\d\.\-]", "", s)  # 숫자, 마침표, 음수부호만 남김
    if s in ["", ".", "-", "-.", ".-"]:
        return None
    try:
        return float(s)
    except Exception:
        return None

# 6) parse rows into list of dicts
data = []
for r in rows:
    # protect index out of range
    n = len(header)
    rowd = {}
    for i, key in enumerate(header):
        rowd[key] = r[i] if i < len(r) else ""
    # normalize
    raw_date = rowd.get(date_col, "").strip()
    raw_gu = rowd.get(gu_col, "").strip()
    raw_hour = rowd.get(hour_col, "").strip()
    raw_pm10 = rowd.get(pm10_col, "").strip()
    # append
    data.append({
        "raw_date": raw_date,
        "raw_gu": raw_gu,
        "raw_hour": raw_hour,
        "raw_pm10": raw_pm10
    })

if not data:
    st.error("CSV에 데이터 행이 없습니다.")
    st.stop()

# 7) 날짜 정규화 (가능하면 날짜 파싱)
def try_parse_date(s):
    s = s.strip()
    if not s:
        return None
    fmts = [
        "%Y-%m-%d", "%Y/%m/%d", "%Y%m%d",
        "%Y-%m-%d %H:%M:%S", "%Y/%m/%d %H:%M:%S",
        "%Y-%m-%d %H:%M", "%Y/%m/%d %H:%M",
        "%Y.%m.%d", "%Y.%m.%d %H:%M"
    ]
    for f in fmts:
        try:
            dt = datetime.strptime(s, f)
            return dt.date().isoformat()  # YYYY-MM-DD
        except Exception:
            continue
    # 어떤 경우 '20241201' 같은 긴 숫자일 수 있음 -> try detect YYYYMMDD
    m = re.match(r"^(20\d{6})", s)
    if m:
        try:
            return datetime.strptime(m.group(1), "%Y%m%d").date().isoformat()
        except Exception:
            pass
    # fallback: if string contains yyyy-mm or yyyy/mm, extract prefix
    m2 = re.search(r"(20\d{2}[-/\.]\d{1,2}[-/\.]\d{1,2})", s)
    if m2:
        try:
            return try_parse_date(m2.group(1))
        except Exception:
            pass
    return s  # 그대로 반환 (문자열 기준 필터링)

for d in data:
    d["date_norm"] = try_parse_date(d["raw_date"])

# 8) 시간 정규화 -> 정수 0~23
def parse_hour(s):
    s = str(s).strip()
    if s == "":
        return None
    # 흔한 형태: "13", "13시", "13:00", "13:00:00", "2024-12-01 13:00"
    m = re.search(r"(\d{1,2})(?=[:시]|$)", s)
    if m:
        try:
            h = int(m.group(1))
            if 0 <= h <= 23:
                return h
        except:
            pass
    # fallback: find any number 0-23
    m2 = re.findall(r"\d{1,2}", s)
    for token in m2:
        try:
            h = int(token)
            if 0 <= h <= 23:
                return h
        except:
            pass
    return None

for d in data:
    d["hour_norm"] = parse_hour(d["raw_hour"])
    d["pm10_val"] = to_float_safe(d["raw_pm10"])

# 9) 사용자에게 사용할 날짜 선택지 보여주기 (정규화된 값 기준)
dates = sorted(list({d["date_norm"] for d in data if d["date_norm"] is not None}))
if not dates:
    st.error("날짜 컬럼에서 유효한 값(예: 2024-12-01)을 찾지 못했습니다. 날짜 컬럼값을 확인하세요.")
    st.stop()

selected_date = st.selectbox("📅 날짜 선택 (정규화된 값)", dates)

# 10) 선택한 날짜에 해당하는 구(지역) 목록
gus = sorted(list({d["raw_gu"] for d in data if d["date_norm"] == selected_date and d["raw_gu"]}))
if not gus:
    st.error("선택한 날짜에 대한 지역(구) 데이터가 없습니다. CSV 내용을 확인해주세요.")
    st.stop()

selected_gu = st.selectbox("🏙️ 구(지역) 선택", gus)

# 11) 선택된 날짜+구에 대해 시간대별 pm10 평균 계산
# create dict hour -> list of pm10
hour_map = {}
for d in data:
    if d["date_norm"] == selected_date and d["raw_gu"] == selected_gu:
        h = d["hour_norm"]
        v = d["pm10_val"]
        if h is None or v is None:
            continue
        hour_map.setdefault(h, []).append(v)

# If no valid hour_map
if not hour_map:
    st.warning("선택한 날짜/구에 유효한 시간대별 PM10 데이터가 없습니다 (시간/값 누락).")
    # show raw rows for debugging
    st.write("해당 필터의 원시 데이터 일부:")
    sample = [d for d in data if d["date_norm"]==selected_date and d["raw_gu"]==selected_gu][:20]
    st.write(sample)
    st.stop()

# create sorted list of hours 0..23 but only those present
hours_sorted = sorted(hour_map.keys())
hour_avg = {h: mean(hour_map[h]) for h in hours_sorted}

st.subheader(f"📊 {selected_date} / {selected_gu} — 시간대별 평균 PM10 (㎍/㎥)")
for h in hours_sorted:
    v = hour_avg[h]
    st.write(f"- **{h}시 → {v:.1f} ㎍/㎥**")

# 12) 외출 추천 로직 (기본 PM10 기준)
good = [f"{h}시" for h, v in hour_avg.items() if v <= 30]
normal = [f"{h}시" for h, v in hour_avg.items() if 31 <= v <= 80]
bad = [f"{h}시" for h, v in hour_avg.items() if v >= 81]

st.subheader("🌤️ 외출 권장 시간대")
if good:
    st.success("✨ 좋은 시간대 (PM10 ≤ 30): " + ", ".join(good))
if normal:
    st.info("🙂 무난한 시간대 (PM10 31~80): " + ", ".join(normal))
if bad and not good:
    st.warning("⚠️ 나쁜 시간대 다수 (PM10 ≥ 81) — 가능한 외출 자제 권장: " + ", ".join(bad[:8]) + ("..." if len(bad)>8 else ""))

# 13) 간단한 요약/권장 문구
best = good[:3]
if best:
    st.write("**요약:** 가장 추천하는 외출 시간대 (최대 3개): " + ", ".join(best))
else:
    st.write("**요약:** 이 날짜/구는 좋은 시간대가 거의 없습니다. 실외 활동을 줄이세요.")

st.write("---")
st.caption("자동 컬럼 매핑이 잘못되었다고 생각하면 위의 드롭다운에서 컬럼을 바꿔주세요. 필요하면 CSV의 상위 20행(원시)을 붙여주시면 더 맞춤 코드를 드립니다.")
