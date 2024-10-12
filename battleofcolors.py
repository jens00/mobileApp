players = []
queue = []

def getPlayers():
  return players

def getQueue():
  return queue

def removePlayerById(client_id: str):
    if client_id in players:
        players.remove(client_id)
