from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise, connections
import uvicorn

from src import settings
from src.bot.api import bot_router
from src.collector.api import messages_router
from src.users.api import users_router
from src.websocket.api import ws_router


app = FastAPI(title="Telegram Collector")
app.include_router(messages_router, prefix="/messages", tags=["messages"])
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(bot_router, prefix="/bot", tags=["bot"])
app.include_router(ws_router, prefix="/ws", tags=["ws"])


@app.on_event("startup")
async def startup():
    register_tortoise(
        app,
        # db_url=settings.POSTGRESQL_URL,
        db_url="sqlite://database/db.sqlite",
        modules={"models": ["src.users.dao", "src.collector.dao",
                            "src.bot.dao"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )

@app.on_event("shutdown")
async def shutdown():
    await connections.close_all()

@app.get("/")
async def read_root():
    return {"Connection": "Success"}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="0.0.0.0", reload=True)