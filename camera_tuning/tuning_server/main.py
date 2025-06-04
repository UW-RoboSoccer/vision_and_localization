import sys
import pathlib

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

origins = []

origins.extend(
    [
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:8085",
    ]
)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
async def redirect_root_to_docs():
    return RedirectResponse("/docs")
