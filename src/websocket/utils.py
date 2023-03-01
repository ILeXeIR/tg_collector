import json
from typing import List

from fastapi import WebSocket

from src.collector.dao import Message


def get_json_from_message(message: Message) -> str:
    #Because of error: 'Object of type UUID is not JSON serializable'
    message_dict = dict(message)
    message_dict["id"] = str(message_dict["id"])
    return json.dumps(message_dict, indent=2)

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

    async def broadcast(self, message: Message, chat_id: int):
        for connection in self.active_connections:
            if connection["chat_id"] == chat_id:
                message_json = get_json_from_message(message)
                await connection["websocket"].send_text(message_json)