from numpy import record

from .BaseDataModel import BaseDataModel
from .enums import DatabaseEnum
from .db_schemes import Project
from bson import ObjectId
from pymongo import InsertOne

class ProjectModel(BaseDataModel):
    def __init__(self, db_client):
        super().__init__(db_client)
        self.collection = self.db_client[DatabaseEnum.COLLECTION_PROJECT_NAME.value]


    async def create_project(self, project: Project):
        result = await self.collection.insert_one(project.model_dump(by_alias=True, exclude_unset=True))
        project.id = result.inserted_id

        return project
    

    async def get_project_or_create_one(self, project_id: str):
        record = await self.collection.find_one({
            "project_id": project_id
        })
        if record is None:
            # Create a new project if it doesn't exist
            project = Project(project_id=project_id)
            project = await self.create_project(project=project )
            return project
        
        return Project(**record) # TODO: we have a problem here, we need to return a Project object, but the record is a dict. We need to convert it to a Project object.
            

    async def get_all_projects(self, page: int = 1, page_size: int = 10):
        # Calculate the number of documents to skip based on the page and page_size
        total_documents = await self.collection.count_documents({})
        total_pages = (total_documents + page_size - 1) // page_size  # Calculate total pages

        cursor = self.collection.find().skip((page - 1) * page_size).limit(page_size)

        projects = []
        async for document in cursor:
            projects.append(Project(**document))

        return projects, total_pages
