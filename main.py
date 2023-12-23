from fastapi import FastAPI, HTTPException
from db_conn import DBConnection
from pydantic import BaseModel
from os import environ
from datetime import date

app = FastAPI()
db = DBConnection(f"mysql://{environ.get('DB_USER')}:{environ.get('DB_PASSWORD')}@{environ.get('DB_HOST')}/{environ.get('DB_NAME')}")


# Base Models for create & update.
class SubtaskPydantic(BaseModel):
    name: str
    completed: bool


class TaskPydantic(BaseModel):
    name: str
    completed: bool
    priority: str
    assignee: str
    due_date: date
    subtasks: list[SubtaskPydantic] = []


class RepositoryPydantic(BaseModel):
    name: str
    tasks: list[TaskPydantic] = []


class ProjectPydantic(BaseModel):
    name: str
    repositories: list[RepositoryPydantic] = []


@app.get("/")
async def root():
    return {"message": "listify_api"}


# ---- CREATE
@app.post("/upload/project")
async def upload_project(project: ProjectPydantic):
    return db.add_project(project.dict())


# ---- READ
@app.get("/get/project/{id}")
async def get_project(id: int):
    return db.get_project_dict_by_id(id)


@app.get("/get/all_projects")
async def get_all_projects():
    return db.get_projects_list()


# --- UPDATE
@app.post("/update/project/{id}")
async def update_project(project: ProjectPydantic, id: int):
    return db.overwrite_project_by_id(id, project.dict())


# ---- DELETE
@app.delete("/delete/{element_type}/{id}")
async def delete(element_type: str, id: int):
    element_type = element_type.capitalize()
    if element_type not in ["Project", "Repository", "Task", "Subtask"]:
        raise HTTPException(status_code=400, detail="Invalid element type")

    return db.delete_element_by_id(element_type, id)
