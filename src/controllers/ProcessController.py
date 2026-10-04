from .BaseController import BaseController
from .ProjectController import ProjectController
from fastapi import UploadFile
from models import ResponseSignal, ProcessingEnum
import os
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

class ProcessController(BaseController):
    def __init__(self, project_id: str):
        super().__init__()

        self.project_id = project_id
        self.project_path = ProjectController().get_project_path(project_id=project_id)

    def get_file_extension(self, file_id: str) -> str:
        return os.path.splitext(file_id)[-1]

    def get_file_loader(self, file_id: str):
        file_extension = self.get_file_extension(file_id)
        file_path = os.path.join(self.project_path, file_id)
        if file_extension == ProcessingEnum.TXT.value:
            return TextLoader(file_path, encoding="utf-8")
        elif file_extension == ProcessingEnum.PDF.value:
            return PyMuPDFLoader(file_path)
        else:
            return None, ResponseSignal.FILE_LOADER_FAILED.value


    def get_file_content(self, file_id: str):
        loader = self.get_file_loader(file_id=file_id)
        if loader is None:
            return None, ResponseSignal.FILE_CONTENT_FAILED.value
        else:
            documents = loader.load()
            return documents, ResponseSignal.SUCCESS.value


    def process_file_content(self, file_id: str, chunk_size: int = 100, chunk_overlap: int = 20):
        documents, message = self.get_file_content(file_id=file_id)
        if documents is None:
            return None, message
        else:
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                length_function=len
            )

            file_content_text = [doc.page_content for doc in documents]
            file_content_metadata = [doc.metadata for doc in documents]

            chunks = text_splitter.create_documents(
                texts=file_content_text,
                metadatas=file_content_metadata
            )
            
            return chunks, ResponseSignal.FILE_PROCESSING_SUCCESS.value