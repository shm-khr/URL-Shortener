from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime
class URLCreate(BaseModel):
    url: HttpUrl
    custom_code : Optional[str] = None
    expires_at : Optional[datetime] = None

class URLResponse(BaseModel):
    short_url: str