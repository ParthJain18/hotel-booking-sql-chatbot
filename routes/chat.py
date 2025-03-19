from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime

from models.database import get_db
from models.chat import get_chat_db
from models.schemas import ChatQuery
from services.process_query import process_query
from services.chat_history import get_all_chat_histories, get_chat_history, create_chat_history, add_message_to_history

router = APIRouter(prefix="/chat", tags=["chat"])
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def chat_page(request: Request, chat_db: Session = Depends(get_chat_db)):
    """Render the chat page with history sidebar"""
    histories = get_all_chat_histories(chat_db)
    return templates.TemplateResponse("chat.html", {
        "request": request,
        "histories": histories
    })

@router.post("/query")
async def query(
    chat_query: ChatQuery,
    chat_db: Session = Depends(get_chat_db)
):
    """Process a query and store in chat history"""
    # Process the query
    result = process_query(chat_query.query)
    
    # Save to chat history
    if chat_query.history_id:  # Get history_id from the request body
        # Add to existing history
        add_message_to_history(chat_db, chat_query.history_id, {
            "content": chat_query.query,
            "is_user": True,
            "timestamp": datetime.utcnow().isoformat()
        })
        add_message_to_history(chat_db, chat_query.history_id, {
            "content": result,
            "is_user": False,
            "timestamp": datetime.utcnow().isoformat()
        })
    else:
        # Create new history
        history = create_chat_history(chat_db, chat_query.query)
        add_message_to_history(chat_db, history.id, {
            "content": result,
            "is_user": False,
            "timestamp": datetime.utcnow().isoformat()
        })
        # Add history ID to result
        result["history_id"] = history.id
    
    return JSONResponse(content=result)

@router.get("/history")
async def get_histories(chat_db: Session = Depends(get_chat_db)):
    """Get all chat histories"""
    histories = get_all_chat_histories(chat_db)
    return JSONResponse(content=histories)

@router.get("/history/{history_id}")
async def get_history(history_id: int, chat_db: Session = Depends(get_chat_db)):
    """Get a specific chat history"""
    history = get_chat_history(chat_db, history_id)
    if not history:
        raise HTTPException(status_code=404, detail="Chat history not found")
    return JSONResponse(content=history)