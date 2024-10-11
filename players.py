from pydantic import BaseModel

playerList = []


class Player(BaseModel):
    id: str

    def display_info(self):
        print("Player Information:")
        print(f"Id: {self.id}")


def getPlayers():
    return playerList
