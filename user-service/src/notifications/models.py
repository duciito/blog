from beanie import Document, Link
from core.models import User


class LikeEvent(Document):
    creator: Link[User]
    user: Link[User]
    obj_id: str
    obj_type: str
