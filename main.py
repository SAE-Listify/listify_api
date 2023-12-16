from fastapi import FastAPI, HTTPException
from db_conn import DBConnection
from pydantic import BaseModel

app = FastAPI()
db = DBConnection("mysql://root:vm@vm.lan/listify_bdd")


# Base Models for create & update
class SubtaskPydantic(BaseModel):
    subtask_id: int
    task_id: int
    name: str
    completed: bool


class TaskPydantic(BaseModel):
    task_id: int
    repository_id: int
    name: str
    completed: bool
    subtasks: list[SubtaskPydantic] = []


class RepositoryPydantic(BaseModel):
    repository_id: int
    project_id: int
    name: str
    tasks: list[TaskPydantic] = []


class ProjectPydantic(BaseModel):
    project_id: int
    name: str
    repositories: list[RepositoryPydantic] = []


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


# ---- READ
@app.get("/get/project/{id}")
async def get_project(id: int):
    return db.get_project_dict_by_id(id)


# ---- DELETE
@app.delete("/delete/{element_type}/{id}")
async def delete(element_type: str, id: int):
    element_type = element_type.capitalize()
    if element_type not in ["Project", "Repository", "Task", "Subtask"]:
        raise HTTPException(status_code=400, detail="Invalid element type")

    return db.delete_element_by_id(element_type, id)
