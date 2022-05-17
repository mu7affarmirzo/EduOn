import asyncio
import os

from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from videoprops import get_video_properties

import shutil

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/stream", response_class=HTMLResponse)
async def stream(request: Request):
    return templates.TemplateResponse("stream.html", {"request": request})


@app.get("/upload", response_class=HTMLResponse)
async def upload(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})


async def segment(input_file: str, output_file: str):
    props = get_video_properties(input_file)
    resolution = "{width}x{height}".format(
        width=props['width'],
        height=props['height']
    )
    await asyncio.create_subprocess_exec(

        "ffmpeg",
        "-i", input_file,
        "-profile:v", "baseline",
        "-level", "3.0",
        "-s", resolution,
        "-start_number", "0",
        "-hls_time", "10",
        "-hls_list_size", "0",
        "-f", "hls", output_file,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )


@app.post("/media/{media_id}/upload")
async def upload(
        media_id: int,
        video: UploadFile = File(
            ...,
            description="video file",
        ),
):
    path = "media/{}/hls".format(media_id)

    is_exist = os.path.exists(path)
    if not is_exist:
        os.makedirs(path)

    file_location = "{}/{}".format(path[:-4], video.filename)

    f = open(file_location, mode='wb+')
    f.write(video.file.read())
    await segment(file_location, "{}/index.m3u8".format(path))
    return {"message": "uploaded successfully"}


@app.delete("/media/{media_id}/delete")
async def delete_video(
        media_id: int,
):
    path = "media/{}/hls".format(media_id)

    is_exist = os.path.exists(path[:-4])
    if is_exist:
        shutil.rmtree(path[:-4])
    return {"message": "deleted successfully"}


@app.get("/media/{media_id}/stream")
async def get_video_index(
        media_id: int,
):
    path = "media/{}/hls".format(media_id)
    index_file = "{}/index.m3u8".format(path)
    return FileResponse(index_file)


@app.get("/media/{media_id}/{segment_name}")
async def get_video_segment(
        media_id: int,
        segment_name: str,
):
    path = "media/{}/hls".format(media_id)
    segment_file = "{}/{}".format(path, segment_name)
    return FileResponse(segment_file)
