# st_chatbot.py
import streamlit as st

import google.generativeai as genai 

import json
import os
from git import Repo # pip install GitPython
from datetime import datetime

# st.title("판다스 AI 챗봇 Test 버젼")
# 
# system_instruction = "당신은 AI 데이터 분석 전문가야. 사용자는 대학원생, 실무자입니다. 쉽고 친절하게 이야기하되 3문장 이내로 짧게 얘기하세요."
# 
# @st.cache_resource
# def load_model():
#     model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_instruction)
#     print("model loaded...")
#     return model
# 
# model = load_model()
# 
# if "chat_session" not in st.session_state:    
#     st.session_state["chat_session"] = model.start_chat(history=[]) 
# 
# for content in st.session_state.chat_session.history:
#     with st.chat_message("ai" if content.role == "model" else "user"):
#         st.markdown(content.parts[0].text)
# 
# if prompt := st.chat_input("메시지를 입력하세요."):    
#     with st.chat_message("user"):
#         st.markdown(prompt)
#     with st.chat_message("ai"):
#         response = st.session_state.chat_session.send_message(prompt)        
#         st.markdown(response.text)
# 
# st.subheader("_당신의 역할을_   :blue[정해주세요!] :sunglasses:")
# 
# left, middle, right = st.columns(3)
# if left.button("기본", use_container_width=True):
#     system_instruction = "당신은 AI 데이터 분석 전문가야. 사용자는 일반인입니다. 쉽고 친절하게 이야기하되 3문장 이내로 짧게 얘기하세요."
#     left.markdown("당신은 일반인입니다.")
# if middle.button("학생", icon="😃", use_container_width=True):
#     system_instruction = "당신은 AI 데이터 분석 전문가야. 사용자는 학생이야. 쉽고 친절하게 이야기하되 3문장 이내로 짧게 얘기하세요."
#     middle.markdown("당신은 학생입니다.")
# if right.button("연구자", icon=":material/mood:", use_container_width=True):
#     system_instruction = "당신은 AI 데이터 분석 전문가야. 사용자는 연구자야. 쉽고 친절하게 이야기하되 3문장 이내로 짧게 얘기하세요."
#     right.markdown("당신은 연구자입니다.")


st.set_page_config(layout="wide")
st.title("OSMnx 원격 계산 요청 앱")

# GitHub 레포지토리 정보 (Streamlit Secrets에서 로드)
# Streamlit Cloud에서 이 앱이 배포된 GitHub 레포지토리의 경로를 사용합니다.
# 즉, 이 앱 자체가 git clone 되어있는 상태이므로, os.getcwd()가 레포지토리 루트입니다.
REPO_DIR = os.getcwd()
INPUT_FILE = os.path.join(REPO_DIR, 'input.json')
OUTPUT_FILE = os.path.join(REPO_DIR, 'output.json')

# GitHub 인증 정보 (Streamlit Secrets에 저장)
GITHUB_TOKEN = st.secrets["github_token"]
GITHUB_USERNAME = st.secrets["github_username"] # 필요시
GITHUB_REPO_OWNER = st.secrets["github_username"] # 또는 조직명
GITHUB_REPO_NAME = "chatbot" # 실제 레포지토리 이름
GITHUB_REPO_URL = f"https://{GITHUB_USERNAME}:{GITHUB_TOKEN}@github.com/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}.git"

# 1. 입력 받기
place_name = st.text_input("분석할 도시 또는 지역 이름:", "Seoul, South Korea")
network_type = st.selectbox("네트워크 타입:", ["drive", "walk", "bike", "all"])

if st.button("계산 요청 및 GitHub에 푸시"):
    # 요청에 고유 ID 및 타임스탬프 추가
    request_id = datetime.now().strftime("%Y%m%d%H%M%S")
    input_data = {
        "request_id": request_id,
        "place_name": place_name,
        "network_type": network_type,
        "timestamp": datetime.now().isoformat()
    }

    with st.spinner("요청을 GitHub에 푸시 중..."):
        try:
            # 현재 디렉토리에서 Git 레포지토리 로드
            repo = Repo(REPO_DIR)

            # input.json 업데이트
            with open(INPUT_FILE, 'w', encoding='utf-8') as f:
                json.dump(input_data, f, ensure_ascii=False, indent=4)

            # 변경사항 커밋 및 푸시
            repo.index.add([INPUT_FILE])
            repo.index.commit(f"Input request ID: {request_id} for {place_name}")

            # 원격 저장소에 푸시 (인증 정보를 포함한 URL 사용)
            # git.cmd.Git 대신 repo.remote(name='origin').push()를 사용할 수 있지만
            # secrets에 포함된 토큰으로 인증하려면 URL에 직접 포함하는 것이 간단합니다.
            with repo.git.custom_environment(GIT_SSH_COMMAND=f"ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no"):
                # 환경 변수를 사용하여 인증 정보를 분리하는 것이 더 안전하지만,
                # 여기서는 URL에 직접 포함하는 예시를 보여줍니다.
                # 실제 배포 시에는 더 안전한 방법을 찾아보시는 것을 권장합니다.
                # GitPython이 SSH를 사용하는 경우, GITHUB_TOKEN을 패스워드로 사용하는 HTTPS URL이 아닌 SSH 키를 사용하는 방식도 고려할 수 있습니다.
                # 간단한 HTTPS 인증을 위해 GitPython이 Git 명령어를 호출하도록 합니다.
                os.system(f'git -c "http.extraheader=AUTHORIZATION: Basic $(echo -n {GITHUB_USERNAME}:{GITHUB_TOKEN} | base64)" -C {REPO_DIR} push origin HEAD')

            st.session_state['last_request_id'] = request_id
            st.success("요청이 성공적으로 GitHub에 푸시되었습니다. 회사 컴퓨터에서 계산 중...")
            st.info("결과가 도착하면 이 페이지가 자동으로 업데이트됩니다.")

        except Exception as e:
            st.error(f"GitHub 푸시 중 오류 발생: {e}")
            st.session_state['last_request_id'] = None

st.header("계산 결과")

# 2. 결과 표시 (GitHub에서 결과 파일 읽기)
# Streamlit Cloud는 GitHub 레포지토리가 업데이트될 때 자동으로 pull하고 앱을 다시 실행합니다.
# 즉, output.json이 변경되면 Streamlit 앱이 재실행되면서 최신 output.json을 읽게 됩니다.
if os.path.exists(OUTPUT_FILE):
    try:
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
            output_data = json.load(f)

        # 마지막 요청 ID와 결과 ID가 일치하는지 확인 (선택 사항)
        if st.session_state.get('last_request_id') and \
           output_data.get('request_id') == st.session_state['last_request_id']:
            st.success(f"요청 ID {output_data['request_id']}에 대한 계산 결과가 도착했습니다!")
            st.session_state['last_request_id'] = None # 처리 완료 표시
        else:
            st.info("최신 계산 결과가 표시됩니다.")

        st.json(output_data)
        # 여기에 Streamlit 지도 시각화 코드 추가 (예: st.map, pydeck, folium)
        # 예: if output_data.get('path_geojson'):
        #         st.write("### 계산된 경로")
        #         # st.map() 또는 Folium 등으로 GeoJSON 시각화
        #         # import folium
        #         # m = folium.Map(location=[...], zoom_start=12)
        #         # folium.GeoJson(output_data['path_geojson']).add_to(m)
        #         # st.components.v1.html(m._repr_html_(), height=500)
        # else:
        #     st.info("시각화할 경로 데이터가 없습니다. (예시 결과)")

        st.write(f"계산된 길이 (예시): {output_data.get('calculated_length_km', 'N/A'):.2f} km")

    except json.JSONDecodeError:
        st.error("output.json 파일이 유효한 JSON 형식이 아닙니다.")
    except Exception as e:
        st.error(f"결과 파일을 읽는 중 오류 발생: {e}")
else:
    st.info("아직 계산 결과가 없습니다. 요청을 보내주세요.")

st.write("---")
st.info("이 앱은 Streamlit Cloud에서 GitHub 레포지토리를 통해 회사 컴퓨터와 데이터를 주고받습니다.")

