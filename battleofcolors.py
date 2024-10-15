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
  players.append(client_id)

  if len(queue) > 0:
    random_player = random.choice(queue)
    websocket = clients.get(random_player)

    if websocket is None:
      print("Error: WebSocket is not initialized.")
      players.remove(client_id)
      return
    
    queue.remove(random_player)

    try:
      number = random.randint(1, 2)
      if number == 1:
        await clients.get(client_id).send_text(f"found player:boc:{random_player}:{client_id}")
        await websocket.send_text(f"found player:boc:{client_id}:{client_id}")
      else:
        await clients.get(client_id).send_text(f"found player:boc:{random_player}:{random_player}")
        await websocket.send_text(f"found player:boc:{client_id}:{random_player}")
    except (asyncio.TimeoutError):
      print("No response from client: " + client_id)
  else:
    queue.append(client_id)

async def endTurn(client_id: str, websocket: WebSocket):
  if websocket is None:
    print("Error: WebSocket is not initialized.")
    
  try:
    await websocket.send_text(f"turn:boc:{client_id}")
  except Exception:
    pass

def removePlayerById(client_id: str):
  if client_id in players:
    players.remove(client_id)
  if client_id in queue:
    queue.remove(client_id)
