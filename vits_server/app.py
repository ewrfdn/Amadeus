from config import AppConfig

from sanic import Sanic, response
from sanic_cors import CORS
from vits_server.blueprints.audio import bp as audio_bp


def serve_error_handle(request, exception):
    if isinstance(exception, Exception):

        if hasattr(exception, "status_code"):
            return response.json(
                {"errorCode": -1, "errorMessage": ",".join(exception.args)}, status=exception.status_code
            )
        else:
            return response.json({"errorCode": -1, "errorMessage": ",".join(exception.args)}, status=400)


app = Sanic("mt-chatdoc")
app.config.TOUCHUP = False
app.config.RESPONSE_TIMEOUT = 60 * 60
CORS(app)

app.blueprint(audio_bp)
app.error_handler.add(Exception, serve_error_handle)


@app.route("/")
async def hi(request):
    print(f"Client-{request.conn_info.client_ip}:{request.conn_info.client_port}: Hi")
    return response.json({"service_name": "vits"})


if __name__ == "__main__":
    app.run(host=AppConfig.HOST, port=AppConfig.PORT)
