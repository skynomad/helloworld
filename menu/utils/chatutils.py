
from typing import Generator
from openai import OpenAI, Stream
from openai.types.chat import ChatCompletion, ChatCompletionChunk

@staticmethod
def stream_response(stream: Stream[ChatCompletionChunk]) -> Generator[str, None, None]:
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

