from fastapi import FastAPI, Query
from typing import Annotated

app = FastAPI()


@app.get("/")
def greet():
    return "Hello World!!"


