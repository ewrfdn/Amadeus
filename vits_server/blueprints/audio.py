import asyncio
import threading
from typing import Tuple
from shortuuid import uuid
from sanic import Blueprint, response
from vits_server.utils.time import current_timestamp
from vits_server.vits_service import VitsService

bp = Blueprint("audio", url_prefix="/audio", version=1)


@bp.route("/text2mp3", methods=["POST", "OPTIONS"])
async def upload_file_to_workspace(request):
    text = request.json.get("text")
    file_name = request.json.get("fileName")
    model = request.json.get("model")
    if file_name is None:
        file_name = f"{current_timestamp('%Y%m%d%H%M%S')}_{uuid()[:5].lower()}"
    vits = VitsService({"model": model})
    path = vits.read_save_mp3(text, file_name)
    return await response.file_stream(path)
