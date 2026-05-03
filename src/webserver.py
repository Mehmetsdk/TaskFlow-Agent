from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Dict
from src.agent import TaskAgent

app = FastAPI()

app.mount("/static", StaticFiles(directory="web"), name="static")

class ChatRequest(BaseModel):
    message: str

agent = TaskAgent()

@app.get("/", response_class=HTMLResponse)
async def index():
    with open("web/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

@app.post("/api/chat")
async def chat(req: ChatRequest):
    resp = agent.process_input(req.message)
    return {"reply": resp}
