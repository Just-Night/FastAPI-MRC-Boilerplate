from pydantic import BaseModel, Field
from datetime import datetime
from core import Config


class TimestampMixin(BaseModel):
    created_at: datetime = Field(default_factory=Config.CURRENT_TIME, allow_mutation=False)
    update_at: datetime = Field(default_factory=Config.CURRENT_TIME)

    class Config:
        from_attributes = True
