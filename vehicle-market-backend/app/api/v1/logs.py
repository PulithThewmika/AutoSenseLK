import logging
import asyncio
import json
from datetime import datetime
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List

router = APIRouter(prefix="/logs", tags=["logs"])

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections.copy():
            try:
                await connection.send_text(message)
            except Exception:
                self.disconnect(connection)

manager = ConnectionManager()

class WebSocketLogHandler(logging.Handler):
    def emit(self, record):
        try:
            log_entry = self.format(record)
            
            # Basic parsing of log message severity
            lvl = record.levelname
            badge = "ok"
            if lvl in ["ERROR", "CRITICAL"]:
                badge = "err"
            elif lvl == "WARNING":
                badge = "warn"

            log_data = {
                "ts": datetime.fromtimestamp(record.created).strftime("%H:%M:%S"),
                "lvl": lvl[:3].upper(),
                "sys": record.name.split('.')[-1] if record.name else "System",
                "msg": record.getMessage(),
                "badge": badge
            }
            # Run broadcast in the current asyncio event loop
            try:
                loop = asyncio.get_running_loop()
                loop.create_task(manager.broadcast(json.dumps(log_data)))
            except RuntimeError:
                pass
        except Exception:
            self.handleError(record)

# Attach handler globally
ws_handler = WebSocketLogHandler()
ws_handler.setLevel(logging.INFO)
logging.getLogger("vehicle_market").addHandler(ws_handler)
logging.getLogger("uvicorn.access").addHandler(ws_handler)
logging.getLogger("uvicorn.error").addHandler(ws_handler)


@router.websocket("/stream")
async def websocket_logs(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        # Send a welcome message
        await websocket.send_text(json.dumps({
            "ts": datetime.now().strftime("%H:%M:%S"),
            "lvl": "INF",
            "sys": "WS",
            "msg": "Connected to real-time log stream.",
            "badge": "ok"
        }))
        while True:
            # Keep connection open
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
