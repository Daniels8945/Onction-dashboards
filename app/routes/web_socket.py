from fastapi import WebSocket, WebSocketDisconnect, APIRouter, Depends
from fastapi.responses import HTMLResponse
import json
from datetime import datetime, timezone, timedelta
from modules.websocket_connection import manager
from models import SubmissionWindow
from typing import Annotated
from sqlmodel import Session
from db.db import get_db
import asyncio
from pydantic import BaseModel, field_validator

router = APIRouter()
SessionInit = Annotated[Session, Depends(get_db)]

@router.get("/ws")
async def get():
    """Serve a simple HTML client for testing"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>WebSocket Test</title>
    </head>
    <body>
        <h1>FastAPI WebSocket Test</h1>
        <form id="form">
            <input type="text" id="msg" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id="messages"></ul>
        <script>
            const ws = new WebSocket("ws://localhost:8000/ws/user123");
            
            ws.onmessage = function(event) {
                const messages = document.getElementById('messages');
                const message = document.createElement('li');
                const data = JSON.parse(event.data);
                message.textContent = `[${data.timestamp}] ${data.message}`;
                messages.appendChild(message);
            };
            
            ws.onopen = function(event) {
                console.log("Connected to WebSocket");
            };
            
            ws.onerror = function(error) {
                console.error("WebSocket error:", error);
            };
            
            document.getElementById('form').onsubmit = function(e) {
                e.preventDefault();
                const input = document.getElementById('msg');
                ws.send(input.value);
                input.value = '';
            };
        </script>
    </body>
    </html>
    """
    return HTMLResponse(html)


class SubmissionWindowInput(BaseModel):
    open_time: datetime
    close_time: datetime

    # @field_validator('open_time', 'close_time', mode='before')
    # def parse_datetime(cls, v):
    #     current_time = timezone(timedelta(hours=1))
    #     if isinstance(v, str):
    #         now = datetime.now(current_time)
    #         minute = (now.minute // 5) * 5
    #         return now.replace(minute= minute, second=0, microsecond=0)
    #     return v
    
    @field_validator('open_time', 'close_time', mode='before')
    def parse_datetime(cls, v):
        if isinstance(v, str):
            return datetime.fromisoformat(v.replace('Z', '+00:00'))
        return v

def  submission_window_time() -> datetime:
            open_time = timezone(timedelta(hours=1))
            now = datetime.now(open_time)
            minute = (now.minute // 5) * 5
            return now.replace(minute= minute, second=0, microsecond=0)

@router.post("/create-submission-window")
def set_window(*, data: SubmissionWindowInput, session: SessionInit):
    window = session.get(SubmissionWindow, 1)


    if not window:
        window = SubmissionWindow(
            id= id(1),
            open_time=data.open_time,
            close_time=data.close_time
        )
        session.add(window)
    else:
        id = window.id + 1
        window.open_time = data.open_time
        window.close_time = data.close_time

    session.commit()
    session.refresh(window)
    return window


@router.get("/get-submission-window")
def get_window(session: SessionInit):
    window = session.query(SubmissionWindow).all()
    return window


@router.delete("/remove-submission-window")
def delete_window(session: SessionInit):
    window = session.get(SubmissionWindow, 1)
    if window:
        session.delete(window)
        session.commit()
    return {"detail": "Submission window deleted"}

@router.put("/submission-window/reset")
def reset_window(session: SessionInit):
    window = session.get(SubmissionWindow, 1)
    if window:
        window.open_time = datetime.utcnow()
        window.close_time = datetime.utcnow()
        session.commit()
        session.refresh(window)
    return window

@router.websocket("/ws/chat")
async def chat_socket(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Chat message: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@router.websocket("/ws/notifications")
async def notifications_socket(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Notification: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@router.websocket("/ws/echo")
async def echo_socket(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You said: {data}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@router.websocket("/ws/countdown")
async def countdown_socket(*,
                           websocket: WebSocket,
                           session: SessionInit
                           ) -> None:

    await manager.connect(websocket)

    window = session.get(SubmissionWindow, 1)

    while True:
        now = datetime.utcnow()
        remaining = (window.close_time - now).total_seconds()

        if remaining <= 0:
            await websocket.send_json({"remaining": 0, "status": "closed"})
            break

        await websocket.send_json({
            "remaining": remaining,
            "status": "open"
        })

        await asyncio.sleep(1)




@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket)
    
    welcome_msg = json.dumps({
        "message": f"Welcome {client_id}! You are connected.",
        "timestamp": datetime.now().strftime("%H:%M:%S")
    })
    await manager.send_personal_message(welcome_msg, websocket)
    
    broadcast_msg = json.dumps({
        "message": f"{client_id} joined the chat",
        "timestamp": datetime.now().strftime("%H:%M:%S")
    })
    await manager.broadcast(broadcast_msg)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            
            # Process and broadcast message
            response = json.dumps({
                "message": f"{client_id}: {data}",
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })
            await manager.broadcast(response)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        disconnect_msg = json.dumps({
            "message": f"{client_id} left the chat",
            "timestamp": datetime.now().strftime("%H:%M:%S")
        })
        await manager.broadcast(disconnect_msg)