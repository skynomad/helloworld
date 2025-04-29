import json
from typing import Generator
from openai import OpenAI, Stream
from openai.types.chat import ChatCompletion, ChatCompletionChunk


class LLMClient:
    def __init__(self, api_key: str, base_url: str):
        """
        OpenAI, LocalAI, Ollama 등의 클라이언트를 초기화합니다.

        Args:
            api_key (str): OpenAI API 키
            base_url (str): API의 기본 URL
        """
        self.llm_client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )

    def list_models(self) -> set:
        """
        사용 가능한 모델 목록을 반환합니다.

        Returns:
            set: 사용 가능한 모델 ID의 집합
        """
        try:
            model_list = self.llm_client.models.list()
            return {model.id for model in model_list}
        except Exception as e:
            print(f"Failed to list models: {e}")
            raise Exception(f"Failed to list models: {e}")

    def generate_response(self, model: str, system_prompt: str, 
        user_prompt: str, max_tokens: int = 1024, stream: bool = True
    ) -> ChatCompletion | Stream[ChatCompletionChunk]:
        """
        스트림 응답을 생성합니다.

        Args:
            model (str): 사용할 모델 이름
            system_prompt (str): 시스템 프롬프트
            user_prompt (str): 사용자 프롬프트
            max_tokens (int): 생성할 최대 토큰 수 (기본값: 1024)
            stream (bool): 스트리밍 여부 (기본값: True)

        Returns:
            generator: 스트리밍 응답 생성기
        """
        try:
            response = self.llm_client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                stream=stream,
                temperature=0,
                max_tokens=max_tokens,
            )
            return response
        except Exception as e:
            raise Exception(f"Failed to generate response: {e}")

    def stream_response(self, stream: Stream[ChatCompletionChunk]) -> Generator[str, None, None]:
        """
        스트리밍 응답을 처리합니다.

        Args:
            completion: 스트리밍 응답 객체

        Yields:
            str: 스트리밍된 텍스트
        """
        for chunk in stream:
            if chunk.choices[0].delta:
                yield chunk.choices[0].delta.content

    def get_response(self, model: str, user_prompt: str, max_tokens: int = 100) -> str:
        """
        사용자 프롬프트에 대한 응답을 생성합니다.

        Args:
            model (str): 사용할 모델 이름
            user_prompt (str): 사용자 프롬프트
            max_tokens (int): 생성할 최대 토큰 수 (기본값: 100)

        Returns:
            str: 생성된 응답 텍스트
        """
        try:
            response = self.llm_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": user_prompt}],
                max_tokens=max_tokens,
                temperature=0,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error: {str(e)}"