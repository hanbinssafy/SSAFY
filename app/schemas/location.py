from pydantic import BaseModel


class LocationCreate(BaseModel):
    name: str
    address: str
    description: str | None = None
    category_name: str | None = None
    image_url: str | None = None


class LocationUpdate(BaseModel):
    name: str
    address: str
    description: str | None = None
    category_name: str | None = None
    image_url: str | None = None


class LocationResponse(BaseModel):
    id: int
    name: str
    address: str
    description: str | None = None
    category_name: str | None = None
    image_url: str | None = None

    class Config:
        from_attributes = True