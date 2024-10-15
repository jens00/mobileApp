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

class BocEndturn(BaseModel):
    id: str
    tile: str
    opponent: str

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

    if client.id in battleofcolors.getPlayers():
        print(f"Client {client.id} is already in the game.")
        return "Client already in the game"
        
    asyncio.run(battleofcolors.addPlayer(client.id, clients))
    return "OK"

@app.post("/boc/endturn")
def boc_endturn(endturn: BocEndturn):
    print(f"Client ID: {endturn.id}")

    if not endturn.id in battleofcolors.getPlayers():
        print(f"Client {endturn.id} is not in a game!")
        return "Client is not in a game"
        
    websocket = clients.get(endturn.opponent)
    self = clients.get(endturn.id)
    asyncio.run(battleofcolors.endTurn(endturn.id, websocket, self))
    return "OK"

@app.get("/boc")
def boc_players():
    return battleofcolors.getPlayers()

@app.get("/privacy")
def privacy_policy():
    with open("privacypolicy.txt", "r") as file:
        html_content = f"""
        <html>
        <head><title>Privacy Policy</title></head>
        <body>
            <h1>Privacy Policy</h1>
            <pre>{file.read()}</pre>
        </body>
        </html>
        """
        return HTMLResponse(content=html_content)

if __name__ == "__main__":
    import uvicorn
    # Start the ping_clients task in the background
    asyncio.run(ping_clients())
    uvicorn.run(app, host="0.0.0.0", port=8205)
