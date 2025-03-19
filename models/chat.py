from sqlalchemy import Column, Integer, String, DateTime, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json
from datetime import datetime

CHAT_DB_URL = "sqlite:///./chat_history.db"
chat_engine = create_engine(CHAT_DB_URL)
ChatSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=chat_engine)
ChatBase = declarative_base()

class ChatHistory(ChatBase):
    __tablename__ = "chat_histories"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True) 
    created_at = Column(DateTime, default=datetime.utcnow)
    messages = Column(Text)
    
    def add_message(self, message, is_user):
        messages_list = json.loads(self.messages) if self.messages else []
        messages_list.append({
            "content": message,
            "is_user": is_user,
            "timestamp": datetime.utcnow().isoformat()
        })
        self.messages = json.dumps(messages_list)
        
        if not self.title and is_user:
            self.title = message[:30] + ("..." if len(message) > 30 else "")
    
def get_chat_db():
    db = ChatSessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_chat_tables():
    ChatBase.metadata.create_all(bind=chat_engine)

if __name__ == "__main__":
    create_chat_tables()