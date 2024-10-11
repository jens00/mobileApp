from fastapi import FastAPI
import players as player

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/boc/add")
async def bocAdd(p: player.Player):
    print(p)
    return p

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8205)
