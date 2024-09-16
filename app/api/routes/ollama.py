from fastapi import APIRouter
from typing import Any, Union
import logging
import ollama
from fastapi.responses import StreamingResponse


logger = logging.getLogger(__name__)
router = APIRouter()

def __pull_streamer(__model: str):
    for part in ollama.pull(
        model=__model,
        stream=True
    ): yield part['status']

def _list():
    return ollama.list()
    

@router.get("/list")
def tags() -> Any:
    return _list()


@router.get("/pull")
def tags(model: Union[str, None] = None) -> Any:
    return StreamingResponse(
        content=__pull_streamer(model.strip()),
        media_type='text/event-stream'
    )
