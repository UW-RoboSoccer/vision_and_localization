import sys
import pathlib

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

sys.path.append(str(pathlib.Path(__file__).resolve().parent))
from routers import camera_router, capture_router, calibrate_router

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

app.include_router(camera_router.router, prefix="/camera", tags=["Camera"])

app.include_router(capture_router.router, prefix="/capture", tags=["Capture"])

app.include_router(calibrate_router.router, prefix="/calibrate", tags=["Calibrate"])


@app.get("/", tags=["Root"])
async def redirect_root_to_docs():
    return RedirectResponse("/docs")
