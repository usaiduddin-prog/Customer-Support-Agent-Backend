from fastapi import FastAPI
from intent_router.__main__ import handle_query

app = FastAPI()

@app.post("/query")
def query(payload: dict):
    return handle_query(payload["query"])