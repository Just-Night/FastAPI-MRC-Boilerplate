
from bson import ObjectId
from pydantic import BaseModel as PydanticBaseModel
from pydantic import Field

from .mixins.timestamp_mixin import TimestampMixin


class DBModel(TimestampMixin, PydanticBaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")

    @classmethod
    def tablename(self):
        return f"{self.__name__.lower()}s"

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
