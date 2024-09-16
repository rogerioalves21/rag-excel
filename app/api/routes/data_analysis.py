from fastapi import APIRouter
from typing import Any, Union
from app.models import ConversationPayload
import logging
from fastapi.responses import StreamingResponse
import ollama
from ollama import ChatResponse
from app.services.data_analysis_service import DataAnalysisService


logger = logging.getLogger(__name__)
router = APIRouter()

def __fake_data(__mensagem: str) -> ChatResponse:
    __data_service = DataAnalysisService()
    __query, __propt = __data_service.chat(__mensagem)
    print(__query, __propt)
    return ollama.chat(
        model='kuqoi/qwen2-tools',
        messages=[
            {'role': 'system', 'content': __propt},
            {'role': 'user', 'content': __query}
        ],
        stream=False,
        keep_alive=0,
        options={ "temperature": 0.3, "repeat_penalty": 1.18, "tfs_z": 2.0, "mirostat": 0,  "repeat_last_n": 64, "num_ctx": 4096, "num_predict": 8192, "low_vram": True, "num_thread": 3, "top_k": 3, "top_p": 0.1, "use_mmap": False }
    )

def __fake_data_streamer(__mensagem: str):
    __data_service = DataAnalysisService()
    __query, __propt = __data_service.chat(__mensagem)
    print(__query, __propt)
    for part in ollama.chat(
        model='llama3-chatqa',
        messages=[
            # {'role': 'system', 'content': __propt},
            {'role': 'user', 'content': __query }
        ],
        stream=True,
        keep_alive=0,
        options={
            "temperature": 0.3,
            "repeat_penalty": 1.18,
            "num_gpu": 0,
            "tfs_z": 2.0,
            "mirostat": 0, 
            "repeat_last_n": 64,
            "num_ctx": 8000,
            "num_predict": 8192,
            "low_vram": True,
            "top_k": 3,
            "top_p": 0.1,
            "use_mmap": False,
            "stop": ["<|eot_id|>", "<|end_of_text|>", "start_header_id|>", "<|end_header_id|>", "<|reserved_special_token"]
        }
    ): yield part['message']['content']  # noqa: E701


@router.post("/data-analysis")
async def chat(__payload: Union[ConversationPayload | None] = None) -> Any:
    return StreamingResponse(
        content=__fake_data_streamer(__payload.properties.question.description.strip()),
        media_type='text/event-stream'
    )

#@router.post("/data-analysis", response_model=NormativosResponse)
#async def chat(__payload: Union[ConversationPayload | None] = None) -> Any:
#    _resp = __fake_data(__payload.properties.question.description.strip())
#    print(f"resposta {_resp['message']['content']}")
#    return NormativosResponse(message=_resp['message']['content'])