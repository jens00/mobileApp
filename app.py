import os
import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8206))  # Default to 8000 if no port is provided
    uvicorn.run(app, host="0.0.0.0", port=port)
