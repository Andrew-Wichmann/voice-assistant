import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.config import Config
from app.session import AudioSession

config = Config()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Pre-load models once at startup rather than per connection
    _session_template = AudioSession(config)
    _session_template.load()
    app.state.config = config
    yield


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def index():
    return FileResponse("static/index.html")


@app.websocket("/ws")
async def audio_stream(websocket: WebSocket):
    await websocket.accept()
    session = AudioSession(app.state.config)
    session.load()

    try:
        async for chunk in websocket.iter_bytes():
            async for message in session.process_chunk(chunk):
                if isinstance(message, dict):
                    await websocket.send_json(message)
                elif isinstance(message, bytes):
                    await websocket.send_bytes(message)
    except WebSocketDisconnect:
        pass
