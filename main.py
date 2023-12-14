from fastapi import FastAPI
from get_proj_by_id import get_project_dict_by_id

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/get/project/{id}")
async def say_hello(id: int):
    return get_project_dict_by_id(id)