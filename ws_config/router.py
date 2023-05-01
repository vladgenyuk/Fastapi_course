import asyncio
import random
import time

from fastapi import APIRouter, WebSocket, WebSocketDisconnect


router = APIRouter(
    prefix='/course',
    tags=['chat']
)


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_json({'data': float(message)})


manager = ConnectionManager()


@router.get('/')
async def get_ws():
    return {'data': 1}


def get_currency(data):
    if random.randint(0, 1):
        return data - random.randint(1, 25) / 5
    return data + random.randint(1, 25) / 5


@router.websocket("/ws/{client_id}")
async def web_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        curr_data = 2000
        await websocket.receive_text()
        while True:
            await websocket.receive_text()
            curr_data = get_currency(curr_data)
            await manager.broadcast(f'{curr_data}')
            time.sleep(1)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        # await manager.broadcast(f'Client #{client_id} left the party')
