import asyncio
from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse
from agent import Agent
app = FastAPI()
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()  # Accept the WebSocket connection
    while True: # Keep the connection open to receive messages
        message = await websocket.receive_text() # Wait for a message from the client
        if message.strip().lower() == "exit": # If the message is "exit", close the connection
            await websocket.close()
            break
        await websocket.send_text(f"Received: {message}")  # Echo the received message back to the client
        response = sock_agent.actions(current_file=None, prompt=message)
        await websocket.send_text(response)  # Send the response back to the client


@app.get("/")
async def get():
    return FileResponse("client.html")
sock_agent = Agent(  #creates an instance of the Agent class and telling it which project we are working on-modified later
    r"C:\Users\orobo\OneDrive\Desktop\Project20 - Copy\SockAI"
)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True) 
    #reload allows my program to restart or reload when a change is made without having to 
    # manually stop and restart the server. This is useful for development and testing, as it allows for 
    # faster iteration and debugging.