import logging
import os
import sys
import tempfile
from urllib.parse import urlparse


from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

logging.basicConfig(level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    buckets = ["test", "test1", "test2"]
    jpeg_dict = {"image_height": 640, "image_width": 480, "make": "NIKON", "is_grayscale": False}
    return templates.TemplateResponse("home.html", {"request": request, "jpeg": jpeg_dict})
