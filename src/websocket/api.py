import json
from typing import List

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

from src.bot.api import send_from_bot
from src.collector.dao import Messages


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[dict] = []

    async def connect(self, websocket: WebSocket, chat_id: int):
        await websocket.accept()
        connection = {
            "websocket": websocket,
            "chat_id": chat_id
        }
        self.active_connections.append(connection)

    def disconnect(self, websocket: WebSocket):
        for connection in self.active_connections:
            if connection["websocket"] == websocket:
                self.active_connections.remove(connection)

    async def broadcast(self, message: Messages, chat_id: int):
        for connection in self.active_connections:
            if connection["chat_id"] == chat_id:
                message_json = json.dumps(dict(message), indent=2)
                await connection["websocket"].send_text(message_json)


ws_router = APIRouter()
manager = ConnectionManager()

"""
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
"""

@ws_router.websocket("/{chat_id}")
async def websocket_chat(websocket: WebSocket, chat_id: int):
    await manager.connect(websocket, chat_id=chat_id)
    chat = await Messages.filter(chat_id=chat_id)
    for message in chat:
        message_json = json.dumps(dict(message), indent=2)
        await websocket.send_text(message_json)
    try:
        while True:
            text = await websocket.receive_text()
            result = await send_from_bot(chat_id=chat_id, text=text)
            if result == "Done!":
                await websocket.send_text(f"Your message was sent:\n'{text}'")
            else:
                await websocket.send_text(f"Error:\n{result}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)