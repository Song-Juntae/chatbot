# st_chatbot.py
import google.generativeai as genai 
import streamlit as st

st.title("판다스 AI 챗봇 Test 버젼")

system_instruction = "당신은 AI 데이터 분석 전문가야. 사용자는 대학원생, 실무자입니다. 쉽고 친절하게 이야기하되 3문장 이내로 짧게 얘기하세요."

@st.cache_resource
def load_model():
    model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_instruction)
    print("model loaded...")
    return model

model = load_model()

if "chat_session" not in st.session_state:    
    st.session_state["chat_session"] = model.start_chat(history=[]) 

for content in st.session_state.chat_session.history:
    with st.chat_message("ai" if content.role == "model" else "user"):
        st.markdown(content.parts[0].text)

if prompt := st.chat_input("메시지를 입력하세요."):    
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("ai"):
        response = st.session_state.chat_session.send_message(prompt)        
        st.markdown(response.text)

st.subheader("_당신의 역할을_   :blue[정해주세요!] :sunglasses:")

left, middle, right = st.columns(3)
if left.button("기본", use_container_width=True):
    system_instruction = "당신은 AI 데이터 분석 전문가야. 사용자는 일반인입니다. 쉽고 친절하게 이야기하되 3문장 이내로 짧게 얘기하세요."
    left.markdown("당신은 일반인입니다.")
if middle.button("학생", icon="😃", use_container_width=True):
    system_instruction = "당신은 AI 데이터 분석 전문가야. 사용자는 학생이야. 쉽고 친절하게 이야기하되 3문장 이내로 짧게 얘기하세요."
    middle.markdown("당신은 학생입니다.")
if right.button("연구자", icon=":material/mood:", use_container_width=True):
    system_instruction = "당신은 AI 데이터 분석 전문가야. 사용자는 연구자야. 쉽고 친절하게 이야기하되 3문장 이내로 짧게 얘기하세요."
    right.markdown("당신은 연구자입니다.")