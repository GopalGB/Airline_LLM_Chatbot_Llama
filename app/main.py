from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse

import uvicorn
import os

from app.api.chatbot_routes import router as chatbot_router

# Create FastAPI app
app = FastAPI(title="Airline Chatbot API")

# Set up templates directory
templates = Jinja2Templates(directory="app/templates")

# Include routers
app.include_router(chatbot_router, prefix="/api", tags=["chatbot"])

# Create templates directory if it doesn't exist
os.makedirs("app/templates", exist_ok=True)

# Create static directory if it doesn't exist
os.makedirs("app/static", exist_ok=True)

# Mount static files directory
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Create HTML template for the chat interface
@app.get("/", response_class=HTMLResponse)
async def get_chat_page(request: Request):
    return templates.TemplateResponse(
        "chat.html", 
        {"request": request, "title": "AirBuddy - Airline Customer Service Chatbot"}
    )

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)