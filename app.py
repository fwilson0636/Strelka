import logging
import sys

from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, HTMLResponse, FileResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI,File ,UploadFile

from models import parse_jpeg_from_path

templates = Jinja2Templates(directory="templates")

logging.basicConfig(level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

app = FastAPI()
app.mount("/static", StaticFiles(directory="files"), name="static")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    buckets = ["test", "test1", "test2"]
    jpeg_dict = {"exifimageheight": 480,
    "exifimagewidth": 640,
    "exifversion": "b'0220'",
    "make": "NIKON",
    "model": "COOLPIX P6000",
    "software": "Nikon Transfer 1.1 W",
    "usercomment": "b'ASCII\\x00\\x00\\x00                                                                                                                     \\x00'",
    "datetime": "2008:11:01 21:15:09",
    "saturation": 0}
    return templates.TemplateResponse("home.html", {"request": request, "jpeg": jpeg_dict})

@app.post("/uploadfile/", response_class=HTMLResponse)
async def create_upload_file(my_file: UploadFile, request: Request):
    print("we made it", my_file)
    
    #contents = await my_file.read()

    if not my_file:
        return {"message":"no file sent to upload file"}
    else:
        info, errors = parse_jpeg_from_path(my_file.file)
        # with open(f"templates/{my_file.filename}",'w+') as image_file:
        #      #with open("my_image.jpeg",'w+') as my_image_file:
        #      image_file.write(str(my_file.file.read()))

        if errors:
            response = {"filename": my_file.filename, "data":info, "errors": errors}
            del errors
            return JSONResponse(response)
        else:
            # return JSONResponse({"filename": my_file.filename, "data": info})
            return templates.TemplateResponse("results.html", {"request": request, "jpeg": info, "img": my_file})
            #return FileResponse(my_file)

    #return HTMLResponse(content=content)
    #return FileResponse(f'./Strelka/files/{my_file}')
    #return FileResponse(my_file.filename)

@app.post("/files/")
async def create_file(file: bytes or None = File(None)):
    if not file:
        return {"message":"no file sent"}
    else:
        return {"file_size": len(file)}
