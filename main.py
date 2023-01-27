import uvicorn
import aerich

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from src.users.endpoints import users_router
from src.db.connect_to_database import connect_to_database
from src import settings


app = FastAPI(title="Telegram Collector")
app.include_router(users_router, prefix="/users", tags=["users"])

await connect_to_database()

@app.on_event("startup")
async def startup():
	await database.connect()

@app.on_event("shutdown")
async def shutdown():
	await database.disconnect()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

register_tortoise(
    app,
    db_url=settings.POSTGRESQL_URL,
    modules={"models": ["src.users.models", "aerich.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)


if __name__ == "__main__":
	uvicorn.run("main:app", port=8000, host="0.0.0.0", reload=True)