from fastapi import APIRouter, UploadFile
from fastapi.responses import Response
from typing import Any
import logging
from app.services.file_service import FilesService

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/files")
async def upload_files(files: list[UploadFile]) -> Any:
    __files_service = FilesService()
    await __files_service.save_content(files)
    return Response(status_code=200)

