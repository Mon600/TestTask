import logging

import uvicorn
from fastapi import FastAPI
from app.api.routers.router import router

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


app = FastAPI(root_path="/api/v1")
logger = logging.getLogger(__name__)

app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app)