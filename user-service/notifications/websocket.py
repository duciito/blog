from typing import Dict
from fastapi import APIRouter, Depends, Query, WebSocket, WebSocketDisconnect
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException

router = APIRouter(prefix='/notifications', tags=["Notifications"])


class NotificationsManager:
    def __init__(self):
        # User id to websocket associaton.
        self.active_connections: Dict[str, WebSocket] = {}

    def add_connection(self, id: str, websocket: WebSocket):
        self.active_connections[id] = websocket

    async def send_text(self, id: str, text: str):
        ws = self.active_connections[id]
        await ws.send_text(text)

    def disconnect(self, id: str):
        if id in self.active_connections:
            del self.active_connections[id]


manager = NotificationsManager()


@router.websocket('/ws')
async def notifications_websocket(websocket: WebSocket,
                                  auth: AuthJWT = Depends(),
                                  token: str = Query()):
    await websocket.accept()
    try:
        await auth.jwt_required_async('websocket', token=token)
        sub = auth.get_jwt_subject()
        manager.add_connection(sub, websocket)
        await manager.send_text(sub, "Successful login!")

        while True:
            # Necessary to detect disconnect events.
            await websocket.receive_text()
    except AuthJWTException as e:
        await websocket.send_text(e.message)
        await websocket.close()
    except WebSocketDisconnect:
        manager.disconnect(sub)
