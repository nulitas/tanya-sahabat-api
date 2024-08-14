from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, validator
from sqlalchemy import Column, Integer, Text, Enum, TIMESTAMP
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from database import SessionLocal, engine, Base
import enum
from typing import Optional
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

class RoleEnum(enum.Enum):
    system = "system"
    user = "user"
    assistant = "assistant"

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(Enum(RoleEnum), nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False, server_default=func.now())  

Base.metadata.create_all(bind=engine)

class MessageCreate(BaseModel):
    role: RoleEnum
    content: str

class MessageResponse(BaseModel):
    id: int
    role: RoleEnum
    content: str
    timestamp: Optional[str]

    @validator("timestamp", pre=True, always=True)
    def convert_timestamp(cls, v):
        if isinstance(v, datetime):
            return v.isoformat()
        return v

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/messages/", response_model=MessageResponse)
def create_message(message: MessageCreate, db: Session = Depends(get_db)):
    db_message = Message(role=message.role, content=message.content)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

@app.get("/messages/", response_model=list[MessageResponse])
def get_messages(db: Session = Depends(get_db)):
    messages = db.query(Message).order_by(Message.timestamp).all()
    return messages

@app.delete("/messages/", status_code=200)
def delete_all_messages(db: Session = Depends(get_db)):
    db.query(Message).delete()
    db.commit()
    return {"message": "All messages have been successfully deleted."}
