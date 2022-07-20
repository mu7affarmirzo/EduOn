import asyncio
import os
import subprocess
from typing import Union

from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from videoprops import get_video_properties
import uuid
import shutil
import nest_asyncio

nest_asyncio.apply()

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


def get_length(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)

async def segment(media_id: int, base_url: str, input_file: str, path: str):
    media_dict = {}
    props = get_video_properties(input_file)

    if int(props['width']) >= 426 and int(props['height']) >= 240:
        media_path = "{}/240p".format(path)
        is_exist = os.path.exists(media_path)
        if not is_exist:
            os.makedirs(media_path)
        proc = await asyncio.create_subprocess_exec(
            "ffmpeg",
            "-i", input_file,
            "-profile:v", "baseline",
            "-level", "3.0",
            "-s", "426x240",
            "-start_number", "0",
            "-hls_time", "1",
            "-hls_list_size", "0",
            "-f", "hls", "{}/index.m3u8".format(media_path),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await proc.wait()
        media_dict['240p'] = f"{base_url}media/{media_id}/240p/stream"

    if int(props['width']) >= 640 and int(props['height']) >= 360:
        media_path = "{}/360p".format(path)
        is_exist = os.path.exists(media_path)
        if not is_exist:
            os.makedirs(media_path)
        proc = await asyncio.create_subprocess_exec(
            "ffmpeg",
            "-i", input_file,
            "-profile:v", "baseline",
            "-level", "3.0",
            "-s", "640x360",
            "-start_number", "0",
            "-hls_time", "1",
            "-hls_list_size", "0",
            "-f", "hls", "{}/index.m3u8".format(media_path),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await proc.wait()
        media_dict['360p'] = f"{base_url}media/{media_id}/360p/stream"

    if int(props['width']) >= 854 and int(props['height']) >= 480:
        media_path = "{}/480p".format(path)
        is_exist = os.path.exists(media_path)
        if not is_exist:
            os.makedirs(media_path)
        proc = await asyncio.create_subprocess_exec(
            "ffmpeg",
            "-i", input_file,
            "-profile:v", "baseline",
            "-level", "3.0",
            "-s", "854x480",
            "-start_number", "0",
            "-hls_time", "1",
            "-hls_list_size", "0",
            "-f", "hls", "{}/index.m3u8".format(media_path),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await proc.wait()
        media_dict['480p'] = f"{base_url}media/{media_id}/480p/stream"

    if int(props['width']) >= 1280 and int(props['height']) >= 720:
        media_path = "{}/720p".format(path)
        is_exist = os.path.exists(media_path)
        if not is_exist:
            os.makedirs(media_path)
        proc = await asyncio.create_subprocess_exec(
            "ffmpeg",
            "-i", input_file,
            "-profile:v", "baseline",
            "-level", "3.0",
            "-s", "1280x720",
            "-start_number", "0",
            "-hls_time", "1",
            "-hls_list_size", "0",
            "-f", "hls", "{}/index.m3u8".format(media_path),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await proc.wait()
        media_dict['720p'] = f"{base_url}media/{media_id}/720p/stream"

    if int(props['width']) >= 1920 and int(props['height']) >= 1080:
        media_path = "{}/1080p".format(path)
        is_exist = os.path.exists(media_path)
        if not is_exist:
            os.makedirs(media_path)
        proc = await asyncio.create_subprocess_exec(
            "ffmpeg",
            "-i", input_file,
            "-profile:v", "baseline",
            "-level", "3.0",
            "-s", "1920x1080",
            "-start_number", "0",
            "-hls_time", "1",
            "-hls_list_size", "0",
            "-f", "hls", "{}/index.m3u8".format(media_path),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await proc.wait()
        media_dict['1080p'] = f"{base_url}media/{media_id}/1080p/stream"

    if int(props['width']) >= 2560 and int(props['height']) >= 1440:
        media_path = "{}/1440p".format(path)
        is_exist = os.path.exists(media_path)
        if not is_exist:
            os.makedirs(media_path)
        proc = await asyncio.create_subprocess_exec(
            "ffmpeg",
            "-i", input_file,
            "-profile:v", "baseline",
            "-level", "3.0",
            "-s", "2560x1440",
            "-start_number", "0",
            "-hls_time", "1",
            "-hls_list_size", "0",
            "-f", "hls", "{}/index.m3u8".format(media_path),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await proc.wait()
        media_dict['1440p'] = f"{base_url}media/{media_id}/1440p/stream"

    if int(props['width']) >= 3840 and int(props['height']) >= 2160:
        media_path = "{}/2160p".format(path)
        is_exist = os.path.exists(media_path)
        if not is_exist:
            os.makedirs(media_path)
        proc = await asyncio.create_subprocess_exec(
            "ffmpeg",
            "-i", input_file,
            "-profile:v", "baseline",
            "-level", "3.0",
            "-s", "3840x2160",
            "-start_number", "0",
            "-hls_time", "1",
            "-hls_list_size", "0",
            "-f", "hls", "{}/index.m3u8".format(media_path),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await proc.wait()
        media_dict['2160p'] = f"{base_url}media/{media_id}/2160p/stream"

    media_dict['duration'] = get_length(input_file)

    return media_dict


@app.post("/media/upload")
async def upload(
        request: Request,
        video: UploadFile = File(
            ...,
            description="video file",
        ),
        subtitle: Union[UploadFile, None] = None,
):
    media_id = uuid.uuid4()
    path = "media/{}/hls".format(media_id)

    is_exist = os.path.exists(path)
    if not is_exist:
        os.makedirs(path)

    if subtitle:
        file_location = "{}/index.srt".format(path[:-4])

        f = open(file_location, mode='wb+')
        f.write(subtitle.file.read())

    file_location = "{}/{}".format(path[:-4], video.filename)

    f = open(file_location, mode='wb+')
    f.write(video.file.read())
    media_dict = asyncio.run(segment(media_id, request.base_url, file_location, path))
    return {"urls": media_dict}


@app.delete("/media/{media_id}/delete")
async def delete_media_folder(
        media_id: str,
):
    path = "media/{}/hls".format(media_id)

    is_exist = os.path.exists(path[:-4])
    if is_exist:
        shutil.rmtree(path[:-4])
    return {"message": "deleted successfully"}


@app.get("/media/{media_id}/{resolution}/stream")
async def get_video_index(
        media_id: str,
        resolution: str,
):
    path = "media/{}/hls/{}".format(media_id, resolution)
    index_file = "{}/index.m3u8".format(path)
    return FileResponse(index_file)


@app.get("/media/{media_id}/{resolution}/{segment_name}")
async def get_video_segment(
        media_id: str,
        resolution: str,
        segment_name: str,
):
    path = "media/{}/hls/{}".format(media_id, resolution)
    segment_file = "{}/{}".format(path, segment_name)
    return FileResponse(segment_file)


@app.get("/media/{media_id}/subtitle")
async def get_video_subtitle(
        media_id: str,
):
    path = "media/{}".format(media_id)
    subtitle_file = "{}/index.srt".format(path)
    return FileResponse(subtitle_file)
