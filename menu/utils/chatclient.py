import json
from typing import Generator
from openai import OpenAI, Stream
from openai.types.chat import ChatCompletion, ChatCompletionChunk

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain.chains import LLMChain

class ChatClient:
    def __init__(self, api_key: str, base_url: str, model: str, streaming: bool = False, temperature: int = 0, max_tokens: int = 1024):
        """
        OpenAI Chat 클라이언트를 초기화합니다.

        Args:
            api_key (str): OpenAI API 키.
            base_url (str): API의 기본 URL.
            model (str): 사용할 모델 이름 (예: "gpt-3.5-turbo").
            streaming (bool): 스트리밍 모드 활성화 여부 (기본값: False).
            temperature (int): 생성된 텍스트의 다양성을 제어하는 값 (기본값: 0).
            max_tokens (int): 생성할 최대 토큰 수 (기본값: 1024).
        """
        self.chat_client = ChatOpenAI(
            api_key=api_key,
            base_url=base_url,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            streaming=streaming,
        )

    def create_llm_chain(self, prompt_template: ChatPromptTemplate, memory: bool = False):
        """
        LLMChain을 생성합니다.

        Args:
            prompt_template (ChatPromptTemplate): LLM에 전달할 프롬프트 템플릿.
            memory (bool): 메모리 사용 여부 (기본값: False).
        """
        self.chain = LLMChain(llm=self.chat_client, prompt=prompt_template, memory=memory)
    
    def create_llm_chain_with_history(self, msgs: StreamlitChatMessageHistory, prompt_template: ChatPromptTemplate, memory: bool = False):
        """
        대화 기록을 포함한 LLMChain을 생성합니다.

        Args:
            msgs (StreamlitChatMessageHistory): Streamlit에서 관리하는 대화 기록 객체.
            prompt_template (ChatPromptTemplate): LLM에 전달할 프롬프트 템플릿.
            memory (bool): 메모리 사용 여부 (기본값: False).
        """
        self.create_llm_chain(prompt_template=prompt_template, memory=memory)
        self.chain_with_history = RunnableWithMessageHistory(
            self.chain,
            lambda session_id: msgs,  # 세션 ID에 따라 대화 기록을 반환하는 함수.
            input_messages_key="question",  # 입력 메시지의 키.
            history_messages_key="history",  # 대화 기록의 키.
        )

    def get_llm_response(self, chain_with_history: RunnableWithMessageHistory, prompt: str) -> str:
        """
        LLM에 프롬프트를 전달하여 응답을 생성합니다.

        Args:
            prompt (str): 사용자 입력 프롬프트.

        Returns:
            str: LLM에서 생성된 응답 텍스트.
        """
        # LangChain이 실행 중에 새 메시지를 자동으로 기록합니다.
        # config={"configurable": {"user_id": "123", "conversation_id": "1"}
        config = {"configurable": {"session_id": "any"}}  # 세션 ID를 설정.
        response = chain_with_history.invoke({"question": prompt}, config)

        return response

    # response = chain_with_history.invoke(
    #     {
    #         "question": "What do you call a parrot that can't speak?" Also, what is my name?",
    #         "language": "Korean"
    #     },
    #     config={"configurable": {"session_id": "1"}},
    # )