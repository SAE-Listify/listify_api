from fastapi import FastAPI
from db_conn import DBConnection

app = FastAPI()
db = DBConnection("mysql://root:vm@vm.lan/listify_bdd")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/get/project/{id}")
async def say_hello(id: int):
    return db.get_project_dict_by_id(id)