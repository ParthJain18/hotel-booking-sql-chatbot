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

    history_id = chat_query.history_id
    if not history_id:
        history = create_chat_history(chat_db, chat_query.query)
        history_id = history.id
    
    add_message_to_history(chat_db, history_id, {
        "content": chat_query.query,
        "is_user": True,
        "timestamp": datetime.utcnow().isoformat()
    })
    
    result = process_query(chat_query.query, history_id)
    
    add_message_to_history(chat_db, history_id, {
        "content": result,
        "is_user": False,
        "timestamp": datetime.utcnow().isoformat()
    })
    
    result["history_id"] = history_id
    
    return JSONResponse(content=result)

@router.get("/history")
async def get_histories(chat_db: Session = Depends(get_chat_db)):
    histories = get_all_chat_histories(chat_db)
    return JSONResponse(content=histories)

@router.get("/history/{history_id}")
async def get_history(history_id: int, chat_db: Session = Depends(get_chat_db)):
    history = get_chat_history(chat_db, history_id)
    if not history:
        raise HTTPException(status_code=404, detail="Chat history not found")
    return JSONResponse(content=history)