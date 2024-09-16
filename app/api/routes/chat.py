from fastapi import APIRouter
from typing import Any, Union
from app.models import ConversationPayload
import logging
from fastapi.responses import StreamingResponse
import ollama
from app.services.data_analysis_service import DataAnalysisService

logger = logging.getLogger(__name__)
router = APIRouter()

def __stream_call(__filename: str, __mensagem: str):
    __data_service = DataAnalysisService()
    __context = __data_service.get_file_content(__filename)
    __query = __data_service.chat_with_file(__context, __mensagem)
    print(__query)
    for part in ollama.chat(
        model="qwen2",
        messages=[
            # {'role': 'system', 'content': __propt},
            {"role": "user", "content": __query}
        ],
        stream=True,
        keep_alive='60m0s',
        options={
            "temperature": 0.3,
            "repeat_penalty": 1.18,
            "num_gpu": 999,
            "tfs_z": 2.0,
            "mirostat": 0,
            "repeat_last_n": 512,
            "num_ctx": 8192,
            "num_predict": 2048,
            "low_vram": True,
            "top_k": 3,
            "top_p": 0.1,
            "use_mmap": False,
        },
    ):
        yield part["message"]["content"]  # noqa: E701


@router.post("/chat")
async def chat(__payload: Union[ConversationPayload | None] = None) -> Any:
    return StreamingResponse(
        content=__stream_call(__payload.file_name, __payload.properties.question.description.strip()),
        media_type='text/event-stream'
    )
