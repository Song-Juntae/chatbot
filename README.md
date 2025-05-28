# chatbot





## model = genai.GenerativeModel("gemini-2.0-flash", system_instruction=system_instruction, generation_config={"response_mime_type": "application/json"})

generation_config

    모델의 응답 생성 방식을 세밀하게 제어하는 설정 모음입니다. None으로 설정하면 기본 생성 설정이 사용됩니다.

    temperature: 텍스트 생성의 무작위성(창의성)을 조절합니다. 값이 높으면 더 다양하고 예측 불가능한 응답이, 낮으면 더 일관되고 보수적인 응답이 생성됩니다.
    top_p: 확률이 높은 단어들 중 누적 확률이 top_p 값에 도달할 때까지 단어를 선택합니다.
    top_k: 다음 단어를 선택할 때 확률이 가장 높은 k개의 단어 중에서만 선택합니다.
    max_output_tokens: 생성될 응답의 최대 토큰(단어) 수를 제한합니다.
    stop_sequences: 특정 문자열이 나타나면 모델의 생성을 중단합니다.
    response_mime_type: 응답의 MIME 타입을 지정하여, 예를 들어 application/json으로 설정하면 JSON 형식의 출력을 유도할 수 있습니다.

tools

    함수 호출(Function Calling) 기능과 관련이 있습니다. 모델이 사용자의 요청을 이해하고, 그 요청을 처리하기 위해 특정 함수를 호출할 필요가 있다고 판단하면, 해당 함수의 이름과 필요한 인자들을 제시합니다. 이를 통해 모델은 실시간 데이터 조회, 계산 수행, 외부 API 호출 등 다양한 기능을 확장할 수 있습니다.

tool_config

    모델이 함수 호출을 수행할 때의 동작을 제어합니다. 예를 들어, 모델이 항상 특정 도구를 사용하도록 강제하거나(강제 호출), 모델이 가장 적절하다고 판단하는 도구를 선택하도록 할 수 있습니다.

system_instruction
    
    모델에게 전반적인 행동 지침이나 역할을 부여하는 명령입니다. 이 지침은 모델이 생성하는 모든 응답에 지속적으로 영향을 미칩니다.
    모델의 페르소나, 스타일, 또는 특정 도메인 지식을 주입하는 데 사용됩니다.