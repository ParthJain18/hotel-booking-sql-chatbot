import datetime
from sqlalchemy.orm import Session
from models.chat import ChatHistory
import json
from typing import List, Dict, Any

def get_all_chat_histories(db: Session) -> List[Dict[str, Any]]:
    """Get all chat histories from DB"""
    histories = db.query(ChatHistory).order_by(ChatHistory.created_at.desc()).all()
    return [
        {
            "id": history.id,
            "title": history.title,
            "created_at": history.created_at.isoformat(),
            "message_count": len(json.loads(history.messages)) if history.messages else 0
        } 
        for history in histories
    ]

def get_chat_history(db: Session, history_id: int) -> Dict[str, Any]:
    """Get a specific chat history by ID"""
    history = db.query(ChatHistory).filter(ChatHistory.id == history_id).first()
    if not history:
        return None
    
    return {
        "id": history.id,
        "title": history.title,
        "created_at": history.created_at.isoformat(),
        "messages": json.loads(history.messages) if history.messages else []
    }

def create_chat_history(db: Session, first_message: str) -> ChatHistory:
    """Create a new chat history"""
    chat_history = ChatHistory(
        title=first_message[:30] + ("..." if len(first_message) > 30 else ""),
        messages=json.dumps([{
            "content": first_message,
            "is_user": True,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }])
    )
    db.add(chat_history)
    db.commit()
    db.refresh(chat_history)
    return chat_history

def add_message_to_history(db: Session, history_id: int, message: Dict[str, Any]) -> bool:
    """Add a new message to an existing chat history"""
    history = db.query(ChatHistory).filter(ChatHistory.id == history_id).first()
    if not history:
        return False
    
    messages = json.loads(history.messages) if history.messages else []
    messages.append(message)
    history.messages = json.dumps(messages)
    
    db.commit()
    db.refresh(history)
    return True