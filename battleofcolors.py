from fastapi import WebSocket
import random

players = []
queue = []

def getPlayers():
  return players

def getQueue():
  return queue

async def addPlayer(client_id: str):
  players.append(client_id)

  if len(queue) > 0:
    random_player = random.choice(queue)
    queue.remove(random_player)

    try:
      await websocket.send_text("found player")
      await asyncio.wait_for(websocket.receive_text(), timeout=10)
    except (asyncio.TimeoutError):
      print("No response from client: " + client_id)
  else:
    queue.append(client_id)
    

def removePlayerById(client_id: str):
    if client_id in players:
        players.remove(client_id)
