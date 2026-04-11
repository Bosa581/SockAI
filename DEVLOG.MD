# SockAI Dev Log

## Issue 1: venv pip not installing to correct location
**Problem:** Had an error with venv, urllib3 needed to be upgraded
**Cause:** The update was being applied to the global Python library instead of inside the venv
**Fix:** Reinstalled pip directly into the venv using the get-pip.py bootstrapper

## Issue 2: Circular import with llamaAPI
**Problem:** Got a circular import error with `from llamaAPI import llamaAPI`
**Cause:** The module and the class inside it had the same name, causing confusion between importing the file vs the class
**Fix:** Changed the import to correctly reference the class inside the module

## Issue 3: uvicorn WebSocket support missing
**Problem:** uvicorn was running but WebSocket connections were failing
**Cause:** The standard uvicorn install doesn't include WebSocket library support
**Fix:** Reinstalled uvicorn with `pip install "uvicorn[standard]"` which includes the required WebSocket dependencies

## Issue 4: Wrong port in client.html
**Problem:** Messages sent from the frontend weren't showing up on screen
**Cause:** VSCode autocomplete filled in port 8080 from a previous project, but the server was running on port 8000
**Fix:** Changed the WebSocket URL in client.html from `ws://localhost:8080/ws` to `ws://localhost:8000/ws`