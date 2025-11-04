import streamlit as st

st.set_page_config(page_title="MBTI 책 & 영화 추천🎬📖", page_icon="🌈")

st.title("🌟 MBTI별 책 & 영화 추천기 🎬📚")
st.write("안녕! 😎 네 MBTI를 골라봐~\n그 유형에 딱 맞는 **책**이랑 **영화**를 추천해줄게 💫")

mbti_list = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP"
]

mbti = st.selectbox("👉 네 MBTI를 선택해줘!", mbti_list)

recommendations = {
    "INTJ": ("『총, 균, 쇠』 - 재레드 다이아몬드", "🎥 인터스텔라"),
    "INTP": ("『사피엔스』 - 유발 하라리", "🎬 인셉션"),
    "ENTJ": ("『원씽(The One Thing)』 - 게리 켈러", "💼 월 스트리트: 머니 네버 슬립스"),
    "ENTP": ("『나의 라임 오렌지나무』 - J.M. 바스콘셀로스", "🔥 아이언맨"),
    "INFJ": ("『연금술사』 - 파울로 코엘료", "💫 어바웃 타임"),
    "INFP": ("『작은 아씨들』 - 루이자 메이 올컷", "💖 월터의 상상은 현실이 된다"),
    "ENFJ": ("『미움받을 용기』 - 기시미 이치로", "🎤 위대한 쇼맨"),
    "ENFP": ("『하루하루가 이별의 날』 - 무라카미 하루키", "🎈 인사이드 아웃"),
    "ISTJ": ("『시간의 역사』 - 스티븐 호킹", "⏰ 덩케르크"),
    "ISFJ": ("『데미안』 - 헤르만 헤세", "🌸 월-E"),
    "ESTJ": ("『7가지 습관』 - 스티븐 코비", "🏢 더 울프 오브 월 스트리트"),
    "ESFJ": ("『트렌드 코리아 2025』 - 김난도 외", "💌 노팅힐"),
    "ISTP": ("『셜록 홈즈 전집』 - 아서 코난 도일", "🕵️‍♂️ 테넷"),
    "ISFP": ("『꽃을 보듯 너를 본다』 - 나태주", "🌿 라라랜드"),
    "ESTP": ("『부의 추월차선』 - 엠제이 드마코", "🚗 분노의 질주"),
    "ESFP": ("『죽고 싶지만 떡볶이는 먹고 싶어』 - 백세희", "🎉 맘마 미아!")
}

if mbti:
    book, movie = recommendations[mbti]
    st.subheader(f"📖 {mbti}에게 어울리는 책:")
    st.write(f"👉 {book}")
    st.subheader(f"🎬 {mbti}에게 찰떡인 영화:")
    st.write(f"👉 {movie}")

st.markdown("---")
st.caption("✨ Made with ❤️ by ChatGPT | 청소년 감성 버전 🌈")
