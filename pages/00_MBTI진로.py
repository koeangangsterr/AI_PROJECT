import streamlit as st

# 제목
st.title("🎯 MBTI로 알아보는 찰떡 진로 추천 💡")

# 설명
st.write("너의 MBTI를 선택하면, 그 성격에 어울리는 진로 2가지를 추천해줄게! 😎")

# MBTI 리스트
mbti_types = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP"
]

# 사용자 입력
selected_mbti = st.selectbox("👇 너의 MBTI를 골라봐!", mbti_types)

# MBTI별 진로 추천 데이터
career_dict = {
    "INTJ": ["데이터 분석가 📊", "전략 컨설턴트 🧠"],
    "INTP": ["연구원 🔬", "프로그래머 💻"],
    "ENTJ": ["CEO 🚀", "경영 컨설턴트 💼"],
    "ENTP": ["창업가 💡", "마케터 📢"],
    "INFJ": ["심리상담사 💬", "작가 ✍️"],
    "INFP": ["예술가 🎨", "교사 🍎"],
    "ENFJ": ["교육자 📚", "커뮤니티 매니저 🤝"],
    "ENFP": ["콘텐츠 크리에이터 🎥", "기획자 📅"],
    "ISTJ": ["공무원 🏛️", "회계사 📘"],
    "ISFJ": ["간호사 🩺", "교사 🍀"],
    "ESTJ": ["관리자 🏢", "프로젝트 매니저 📂"],
    "ESFJ": ["HR매니저 👥", "사회복지사 🤗"],
    "ISTP": ["엔지니어 🔧", "정비사 🛠️"],
    "ISFP": ["디자이너 🎨", "요리사 🍳"],
    "ESTP": ["세일즈 전문가 💬", "스포츠 트레이너 🏋️‍♂️"],
    "ESFP": ["연예인 🎤", "이벤트 플래너 🎉"]
}

# 선택 후 결과 출력
if selected_mbti:
    st.subheader(f"🌈 {selected_mbti} 유형에게 어울리는 진로는...")
    careers = career_dict[selected_mbti]
    st.success(f"1️⃣ {careers[0]}\n\n2️⃣ {careers[1]}")
    st.write("너랑 진짜 잘 어울릴 것 같아! 🔥")
