from fastapi import FastAPI, HTTPException
from db_conn import DBConnection
from pydantic import BaseModel

app = FastAPI()
db = DBConnection("mysql://root:vm@vm.lan/listify_bdd")


# Base Models for create & update
class SubtaskPydantic(BaseModel):
    name: str
    completed: bool


class TaskPydantic(BaseModel):
    name: str
    completed: bool
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
