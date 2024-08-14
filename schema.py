from pydantic import validator

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
