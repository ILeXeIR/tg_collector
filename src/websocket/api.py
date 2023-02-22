import json
from typing import List

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

from src.collector.dao import Messages


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message):
        for connection in self.active_connections:
            message_json = json.dumps(dict(message), indent=2)
            await connection.send_text(message_json)


ws_router = APIRouter()
manager = ConnectionManager()

with open("src/websocket/example.html") as fileobject:
    html = fileobject.read()

@ws_router.get("/")
async def read_root():
    return HTMLResponse(html)

@ws_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")

@ws_router.websocket("/{chat_id}")
async def websocket_chat(websocket: WebSocket, chat_id: int):
    await manager.connect(websocket)
    chat = await Messages.filter(chat_id=chat_id)
    for message in chat:
        message_json = json.dumps(dict(message), indent=2)
        await websocket.send_text(message_json)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Your message: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)