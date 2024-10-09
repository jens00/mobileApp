from fastapi import FastAPI
import servers as server

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/servers")
async def servers():
    print(server.serverList)
    return server.getServers()


@app.post("/servers/add")
async def addServer(s: server.Server):
    server.serverList.append(s)
    print(s)
    return s
