from fastapi import WebSocket
from typing import Dict
import random
import asyncio

players = []
queue = []

def getPlayers():
  return players

def getQueue():
  return queue

async def addPlayer(client_id: str, clients: Dict[str, WebSocket]):
  if websocket is None:
        print("Error: WebSocket is not initialized.")
        return
    
  players.append(client_id)

  if len(queue) > 0:
    random_player = random.choice(queue)
    websocket = clients.get(random_player)
    queue.remove(random_player)

    try:
      await clients.get(client_id).send_text("found player:boc")
      await websocket.send_text("found player:boc")
    except (asyncio.TimeoutError):
      print("No response from client: " + client_id)
  else:
    queue.append(client_id)
    

def removePlayerById(client_id: str):
    if client_id in players:
        players.remove(client_id)
