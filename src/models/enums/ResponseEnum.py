from enum import Enum


class ResponseSignal(Enum):
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"
    WARNING = "WARNING"
    FILE_TYPE_NOT_SUPPORTED = "file_type_not_supported"
    FILE_SIZE_EXCEEDED = "file_size_exceeded"
    FILE_UPLOADED_SUCCESS = "file_uploaded_successfully"
    FILE_UPLOADED_FAILED = "file_uploaded_failed"
    FILE_VALIDATED_SUCCESS = "file_validated_successfully"
    FILE_PROCESSING_FAILED = "file_processing_failed"
    FILE_PROCESSING_SUCCESS = "file_processing_successfully"
    FILE_LOADER_FAILED = "file_loading_failed"
    FILE_CONTENT_FAILED = "file_content_failed"
    FILE_CHUNKING_FAILED = "file_chunking_failed"
