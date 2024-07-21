import os

from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.routes.todos import router as todos_router
from app.routes.users import router as users_router
from app.database.main import init_models

from dotenv import load_dotenv

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await init_models()
        yield
    finally:
        pass


app = FastAPI()

origins = [
    os.getenv("FRONTEND_URI"),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(todos_router, prefix="/api")
app.include_router(users_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
