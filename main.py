from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()
users = {}

from fastapi.staticfiles import StaticFiles
from pathlib import Path

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")


from fastapi import UploadFile, File
import uuid

MAX_BYTES = 10 * 1024 * 1024  

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    try:
        data = await file.read()
        if len(data) > MAX_BYTES:
            return {"ok": False, "error": "File too large (max 10MB)"}

        if not file.filename:
            return {"ok": False, "error": "No filename provided"}

        ext = Path(file.filename).suffix.lower()
        
        allowed = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".pdf", ".txt", ".zip"}
        if ext not in allowed:
            return {"ok": False, "error": f"Not allowed: {ext}"}

        new_name = f"{uuid.uuid4().hex}{ext}"
        out_path = UPLOAD_DIR / new_name
        out_path.write_bytes(data)

        return {
            "ok": True,
            "url": f"/uploads/{new_name}",
            "filename": file.filename,
            "content_type": file.content_type,
            "size": len(data),
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}



@app.get("/", response_class=HTMLResponse)
def home():
    with open("index.html") as f:
        return f.read()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    name = (websocket.query_params.get("name", "unknown") or "unknown").strip()

    await websocket.accept()

    if len(users) >= 2:
        await websocket.send_text("[SYS] Chat room full. Try later.")
        await websocket.close()
        return

    users[websocket] = name

    for u in users:
        if u is not websocket:
            await u.send_text(f"[SYS] {name} joined")

    try:
        while True:
            message = await websocket.receive_text()

            try:
                import json
                msg_data = json.loads(message)
                if msg_data.get("type") == "file":
                    msg_data["sender"] = name
                    broadcast_msg = json.dumps(msg_data)
                    for u in users:
                        if u is not websocket:
                            await u.send_text(broadcast_msg)
                    continue
            except:
                pass

            for u in users:
                if u is not websocket:
                    await u.send_text(f"[{name}] {message}")

    finally:
 
        left_name = users.pop(websocket, name)
        
        for u in users:
            await u.send_text(f"[SYS] {left_name} left")

