from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.crud.category import get_categories
from app.schemas.category import CategoryResponse

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


@router.get("/", response_model=list[CategoryResponse])
def read_categories(db: Session = Depends(get_db)):
    return get_categories(db)