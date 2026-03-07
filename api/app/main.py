from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
import logging
from os import environ
from fastapi import FastAPI, Request
from dotenv import load_dotenv
from sqlmodel import SQLModel
from app import routers
from app.database import construct_tables, engine

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # app startup
    SQLModel.metadata.create_all(engine)
    construct_tables()

    yield
    # app shutdown


app = FastAPI(lifespan=lifespan)

app.include_router(routers.router)

## Middleware

supported_cors_protocols = [
    "http",
    "https",
]
supported_cors_domains = [
    environ.get("CLIENT_ORIGIN_DOMAIN"),
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        f"{protocol}://{domain}"
        for protocol in supported_cors_protocols
        for domain in supported_cors_domains
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_origin(request: Request, call_next):
    print("ORIGIN:", request.headers.get("origin"))
    return await call_next(request)
