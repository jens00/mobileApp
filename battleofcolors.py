from fastapi import WebSocket
import random
import asyncio

players = []
queue = []

def getPlayers():
  return players

def getQueue():
  return queue

async def addPlayer(client_id: str, clients: Dict[str, WebSocket]):
  print("Adding player")
  players.append(client_id)

  if len(queue) > 0:
    random_player = random.choice(queue)
    queue.remove(random_player)

    try:
      await websocket.send_text("found player")
    except (asyncio.TimeoutError):
      print("No response from client: " + client_id)
  else:
    queue.append(client_id)
    

def removePlayerById(client_id: str):
    if client_id in players:
        players.remove(client_id)
