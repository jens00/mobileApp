from pydantic import BaseModel

serverList = []


class Server(BaseModel):
    id: str
    players: list
    isPrivate: bool
    code: str

    def display_info(self):
        print("Server Information:")
        print(f"Id: {self.id}")
        print(f"Players: {self.players}")
        print(f"Private: {self.isPrivate}")
        print(f"Code: {self.code}")


def getServers():
    return serverList
