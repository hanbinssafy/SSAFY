from pydantic import BaseModel


class PostCreate(BaseModel):
    title: str
    content: str
    password: str
    category_id: int


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    category_id: int

    class Config:
        from_attributes = True

class PostUpdate(BaseModel):
    title: str
    content: str
    password: str
    category_id: int