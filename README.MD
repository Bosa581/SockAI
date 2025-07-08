## SockAI

SockAI is a lightweight, local client-server chatbot that uses socket programming to send user prompts to a LLaMA-based AI model running on a local server (via ollama) and receive contextual responses in real-time.

## Goaol
Learn python
Learn the basics of socket/network programming
Practive real time data exchange between client and server
Constructing and sending HTTP requests to a locally hosted LLM (like LLaMA)
Managing conversational context and state between multiple turns of a chat.
Learn how to integrate an ai api with python
Further learning on working with json objects

## Features
Local, socket-based communication (TCP)
Persistent multi-turn AI conversations
Dynamic payload creation with or without conversation history
LLaMA 3 model integration using the http://localhost:11434/api/chat API
Simple and readable architecture for learning and extensibility

## How It Works
The Client sends user prompts to the server using a TCP socket connection.
The Server forwards the prompt to the LLaMA API, which generates an AI response.
The response is sent back over the socket and printed by the client.
Memory is retained between turns using past user-AI exchanges to keep the conversation contextual.

## Challenges Overcome

This project was built through trial, debugging, and persistence. A few notable challenges resolved during development:
Connection Stability: Debugged and fixed [WinError 10053] errors due to premature socket closures.
Payload Flexibility: Implemented dual-payload logic to support both first-turn prompts and multi-turn history without breaking the LLaMA API's structure.
Print Response Timing: Fixed an issue where the AI’s first response was skipped by ensuring correct order and response handling on both client and server ends.
 Conversation State Management: Designed a minimal state system in the llamaAPI class to store the previous user and assistant turns between messages.

## How to Run
🗅 Requirements
Python 3.10+
Ollama installed and running locally (with a model like llama3)
LLaMA model downloaded and running via:
ollama run llama3

## Installation

Clone the repo:
git clone https://github.com/yourusername/SockAI.git
cd SockAI
Start the server:
python Server.py
In a separate terminal, start the client:
python Client.py

## File Structure

SockAI/
├── Client.py         # Handles user input and communication
├── Server.py         # Connects to client and queries LLaMA
├── llamaAPI.py       # Interacts with the local LLaMA model
└── README.md         # Project documentation

## Notes

Uses a buffer size of 8192 bytes—be mindful of this when scaling up response lengths.
This project uses only public methods and APIs and does not require any OpenAI keys or internet access for inference.

## Built With

Python socket module
requests for HTTP communication
LLaMA 3 via ollama

## License
© 2025 Orobosa Igbinovia. Free to use, extend, and improve under open project learning principles.

