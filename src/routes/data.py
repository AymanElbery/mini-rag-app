from fastapi import FastAPI, APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse
import os
from helpers.config import get_settings, Settings
from controllers import DataController, ProjectController, ProcessController
from models import ResponseSignal
import aiofiles
import logging
from .schemes import ProccessRequest

logger = logging.getLogger('uvicorn.error')

app = FastAPI()

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["Data"]
)

@data_router.post("/upload/{project_id}")
async def upload_data(
    project_id: str,
    file: UploadFile,
    app_settings: Settings = Depends(get_settings)
):
    data_controller = DataController()
    valid, message = data_controller.validate_uploaded_file(file = file)

    if not valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": message,
                "project_id": project_id
            }
        )  
    
    file_path, file_id = data_controller.generate_unique_file_path(original_file_name=file.filename, project_id=project_id)

    try:
        async with aiofiles.open(file_path, "wb") as buffer:
            while chunk := await file.read(app_settings.file_default_chunk_size):
                await buffer.write(chunk)
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": ResponseSignal.FILE_UPLOADED_FAILED.value,
                "project_id": project_id
            }
        )
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": ResponseSignal.FILE_UPLOADED_SUCCESS.value,
            "file_name": file.filename,
            "file_id": file_id,
            "project_id": project_id
        }
    )

@data_router.post("/process/{project_id}")
async def process_data(
    project_id: str,
    request: ProccessRequest
):
    process_controller = ProcessController(project_id=project_id)
    file_id = request.file_id
    chunk_size = request.chunk_size
    chunk_overlap = request.overlap_size
    
    try:
        chunks, message = process_controller.process_file_content(
            file_id=file_id,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

        if chunks is None or len(chunks) == 0:
            return JSONResponse(
                status_code=ResponseSignal.FILE_CHUNKING_FAILED.value,
                content={
                    "error": message,
                    "project_id": project_id
                }
            )

        return chunks
    
    except Exception as e:
        logger.error(f"Error processing file: {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": ResponseSignal.FILE_PROCESSING_FAILED.value,
                "project_id": project_id
            }
        )