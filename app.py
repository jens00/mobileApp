from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from typing import Dict
from pydantic import BaseModel
import asyncio

import battleofcolors

app = FastAPI()
clients: Dict[str, WebSocket] = {}  # Dictionary to hold client ID and WebSocket connection

class Client(BaseModel):
    id: str

# Function to send ping and check response
async def ping_clients():
    while True:
        await asyncio.sleep(60)  # Wait for 1 minute before sending the next ping
        for client_id, websocket in list(clients.items()):
            try:
                await websocket.send_text("ping: Are you alive?")
                # Wait for a pong response
                await asyncio.wait_for(websocket.receive_text(), timeout=10)
            except (asyncio.TimeoutError, WebSocketDisconnect):
                # Client didn't respond or disconnected, remove them
                print(f"Client {client_id} did not respond. Removing from list.")
                clients.pop(client_id)

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    clients[client_id] = websocket  # Store the WebSocket connection

    try:
        while True:
            # Wait for pong response
            message = await websocket.receive_text()
            if message == "pong":
                print(f"Client {client_id} is still alive.")
    except WebSocketDisconnect:
        battleofcolors.removePlayerById(client_id)
        print(f"Client {client_id} disconnected.")
        clients.pop(client_id, None)

@app.get("/")
def read_root():
    return HTMLResponse("<h1>WebSocket Server Running</h1>")

@app.post("/boc/add")
def boc_add(client: Client):
    print(f"Client ID: {client.id}")
    websocket = clients.get(client.id)
    asyncio.run(battleofcolors.addPlayer(client.id, clients))
    return "OK"

@app.get("/boc")
def boc_players():
    return battleofcolors.getPlayers()

@app.get("/privacy")
def privacy_policy():
    with open("privacypolicy.txt", "r") as file:
        # Render the privacy policy using a simple HTML template
        return HTMLResponse("<html><head><title>Privacy Policy</title></head><body><pre>{{ policy_text }}</pre></body></html>")

if __name__ == "__main__":
    import uvicorn
    # Start the ping_clients task in the background
    asyncio.run(ping_clients())
    uvicorn.run(app, host="0.0.0.0", port=8205)
