from fastapi import FastAPI, APIRouter, Depends, UploadFile, status, Request
from fastapi.responses import JSONResponse
import os

from httpcore import request
from helpers.config import get_settings, Settings
from controllers import DataController, ProjectController, ProcessController
from models.enums import ResponseSignal
import aiofiles
import logging
from .schemes import ProccessRequest
from models import ProjectModel, ChunkModel
from models.db_schemes import DataChunk

logger = logging.getLogger('uvicorn.error')

app = FastAPI()

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["Data"]
)

@data_router.post("/upload/{project_id}")
async def upload_data(
    request: Request,
    project_id: str,
    file: UploadFile,
    app_settings: Settings = Depends(get_settings)
):
    data_controller = DataController()
    project_model = ProjectModel(db_client=request.app.db_client)

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

    project = await project_model.get_project_or_create_one(project_id=project_id)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": ResponseSignal.FILE_UPLOADED_SUCCESS.value,
            "file_name": file.filename,
            "file_id": file_id,
            "project_id": str(project.id),
        }
    )

@data_router.post("/process/{project_id}")
async def process_data(
    request: Request,
    project_id: str,
    processRequest: ProccessRequest
):
    process_controller = ProcessController(project_id=project_id)
    file_id = processRequest.file_id
    chunk_size = processRequest.chunk_size
    chunk_overlap = processRequest.overlap_size
    do_reset = processRequest.do_reset
    
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
        
        project_model = ProjectModel(db_client=request.app.db_client)
        chunk_model = ChunkModel(db_client=request.app.db_client)

        project = await project_model.get_project_or_create_one(project_id=project_id)
        
        chunks_records = [
            DataChunk(
                chunk_text=chunk.page_content,
                chunk_metadata=chunk.metadata,
                chunk_order=i + 1,
                chunk_project_id=project.id
            )
            for i, chunk in enumerate(chunks)
        ]

        

        if do_reset:
            deleted_count = await chunk_model.delete_chunks_by_project_id(project_id=project.id)
        else:
            deleted_count = 0

        no_records_inserted = await chunk_model.insert_many_chunks(chunks=chunks_records)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": ResponseSignal.FILE_PROCESSED_SUCCESS.value,
                "project_id": str(project.id),
                "chunks_inserted": no_records_inserted,
                "chunks_deleted": deleted_count
            }
        )
    
    except Exception as e:
        logger.error(f"Error processing file: {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": ResponseSignal.FILE_PROCESSING_FAILED.value,
                "project_id": project_id
            }
        )