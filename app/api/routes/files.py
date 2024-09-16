from fastapi import APIRouter, UploadFile
from fastapi.responses import Response
from typing import Any, Union
from app.models import FileResponse, FileRequest
from app.services.data_analysis_service import DataAnalysisService
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/documentos/")
async def upload_files(files: list[UploadFile]) -> Any:
    __data_service = DataAnalysisService()
    await __data_service.write_content_files(files)
    return Response(status_code=200)

@router.post("/files", response_model=FileResponse)
def insert_file(__payload: Union[FileRequest, None] = None) -> Any:
    print(f"incluindo o arquivo: {__payload.file_name}")
    return FileResponse(weaviate_id="dsadf", user_id="rogerio.rodrigues")


@router.get("/files", response_model=FileResponse)
def get_files() -> Any:
    return FileResponse(weaviate_id="dsadf", user_id="rogerio.rodrigues")
