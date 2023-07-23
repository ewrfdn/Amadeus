from shortuuid import uuid
from sanic import Blueprint, response
from src.utils.time import current_timestamp
from src.vits_service import VitsService

bp = Blueprint("audio", url_prefix="/vits", version=1)


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


@bp.route("/models", methods=["get", "OPTIONS"])
async def get_models(request):
    res = VitsService.get_model_list()
    return response.JSONResponse(res)
