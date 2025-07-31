import uvicorn
from fastapi import FastAPI
from app.api.routers.router import router


app = FastAPI(root_path="/api/v1")

app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app)