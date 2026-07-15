from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.location import LocationCreate, LocationResponse, LocationUpdate
from app.crud.location import (
    create_location,
    get_locations,
    get_location,
    update_location,
    delete_location as delete_location_crud,
)

router = APIRouter(
    prefix="/locations",
    tags=["Locations"]
)


@router.get("/", response_model=list[LocationResponse])
def read_locations(db: Session = Depends(get_db)):
    return get_locations(db)


@router.get("/{location_id}", response_model=LocationResponse)
def read_location(location_id: int, db: Session = Depends(get_db)):
    location = get_location(db, location_id)

    if location is None:
        raise HTTPException(status_code=404, detail="장소가 없습니다.")

    return location


@router.post("/", response_model=LocationResponse)
def write_location(location: LocationCreate, db: Session = Depends(get_db)):
    return create_location(db, location)


@router.put("/{location_id}", response_model=LocationResponse)
def edit_location(location_id: int, location: LocationUpdate, db: Session = Depends(get_db)):
    result = update_location(db, location_id, location)

    if result is None:
        raise HTTPException(status_code=404, detail="장소가 존재하지 않습니다.")

    return result


@router.delete("/{location_id}", response_model=dict)
def remove_location(location_id: int, db: Session = Depends(get_db)):
    result = delete_location_crud(db, location_id)

    if result is None:
        raise HTTPException(status_code=404, detail="장소가 존재하지 않습니다.")

    return {"message": "장소가 삭제되었습니다."}