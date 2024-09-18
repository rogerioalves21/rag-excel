from fastapi import APIRouter
from typing import Any, Union
from app.models import ConversationPayload
import logging
from fastapi.responses import StreamingResponse
import ollama
from app.services.data_analysis_service import DataAnalysisService
from app.services.file_service import FilesService
from app.services.prompt_service import PromptService

logger = logging.getLogger(__name__)
router = APIRouter()

def __stream_call(__filename: str, __mensagem: str):
    __data_service = DataAnalysisService()
    __files_service = FilesService()
    __prompt_service = PromptService()
    __context = __files_service.get_content(__filename)
    __query = __data_service.chat_with_text_file(__context, __mensagem)
    __query = __query[:4096]
    print(__query)
    for part in ollama.chat(
        model="gemma2:2b",
        messages=[
            {'role': 'system', 'content': __prompt_service.get_system_prompt_texto()},
            {"role": "user", "content": __query[:4096]}
        ],
        stream=True,
        keep_alive='0',
        options={
            "temperature": 0.5,
            "repeat_penalty": 1.18,
            # "num_gpu": 999,
            "tfs_z": 2.0,
            "mirostat": 0,
            "repeat_last_n": 64,
            "num_ctx": 4096,
            "num_predict": 1024,
            "low_vram": True,
            "top_k": 3,
            "top_p": 0.1,
            "use_mmap": False,
            # "stop": ["<|eot_id|>", "<|end_of_text|>"]
        },
    ):
        yield part["message"]["content"]  # noqa: E701


@router.post("/chat")
async def chat(__payload: Union[ConversationPayload | None] = None) -> Any:
    return StreamingResponse(
        content=__stream_call(__payload.file_name, __payload.properties.question.description.strip()),
        media_type='text/event-stream'
    )
