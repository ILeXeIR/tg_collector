import json

from fastapi import WebSocket, WebSocketDisconnect

from src.bot.api import send_from_bot
from src.collector.dao import Message
from .deps import get_json_from_message, manager, ws_router


@ws_router.websocket("/{chat_id}")
async def websocket_chat(websocket: WebSocket, chat_id: int):
    await manager.connect(websocket, chat_id=chat_id)
    chat = await Message.filter(chat_id=chat_id)
    for message in chat:
        message_json = get_json_from_message(message)
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