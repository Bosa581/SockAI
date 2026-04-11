from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse
app = FastAPI()
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()  # Accept the WebSocket connection
    while True: # Keep the connection open to receive messages
        message = await websocket.receive_text() # Wait for a message from the client
        if message.strip().lower() == "exit": # If the message is "exit", close the connection
            await websocket.close()
            break
        await websocket.send_text(f"Message received: {message}")  # Echo the received message back to the client

@app.get("/")
async def get():
    return FileResponse("client.html")
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)