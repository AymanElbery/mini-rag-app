from .BaseController import BaseController
from fastapi import UploadFile
from models import ResponseSignal
from .ProjectController import ProjectController
import re
import os

class DataController(BaseController):

    converter_scale = 1024 * 1024

    def __init__(self):
        super().__init__()

    def validate_uploaded_file(self, file: UploadFile):
        if file.content_type not in self.app_settings.file_allowed_types:
            return False, ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value
        
        if file.size > self.app_settings.file_max_size * self.converter_scale:
            return False, ResponseSignal.FILE_SIZE_EXCEEDED.value
        
        return True, ResponseSignal.FILE_VALIDATED_SUCCESS.value
    
    def generate_unique_file_path(self, original_file_name: str, project_id: str):
        random_key = self.generate_random_string(12)
        project_path = ProjectController().get_project_path(project_id)

        new_file_path = os.path.join(project_path, f"{random_key}_{self.clean_file_name(original_file_name)}")
        while os.path.exists(new_file_path):
            random_key = self.generate_random_string(12)
            new_file_path = os.path.join(project_path, f"{random_key}_{self.clean_file_name(original_file_name)}")
            

        return new_file_path, f"{random_key}_{self.clean_file_name(original_file_name)}"
    
    def clean_file_name(self, file_name: str):
        # remove any special characters except _ and .
        cleaned_filename = re.sub(r"[^\w.]", "", file_name.strip())

        # replace any space with _
        cleaned_filename = cleaned_filename.replace(" ", "_")

        return cleaned_filename

