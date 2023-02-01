import uvicorn

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise, connections
from src.users.api import users_router
from src import settings


app = FastAPI(title="Telegram Collector")
app.include_router(users_router, prefix="/users", tags=["users"])

@app.on_event("startup")
async def startup():
    register_tortoise(
        app,
        #db_url=settings.POSTGRESQL_URL,
        db_url="sqlite://database/db.sqlite",
        modules={"models": ["src.users.dao"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )


@app.on_event("shutdown")
async def shutdown():
    await connections.close_all()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
	uvicorn.run("main:app", port=8000, host="0.0.0.0", reload=True)