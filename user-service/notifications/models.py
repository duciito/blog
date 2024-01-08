from beanie import Document, Indexed, Link

from core.models import User


class LikeEvent(Document):
    creator: Indexed(Link[User])
    user: Link[User]
    obj_id: str
    obj_type: str
