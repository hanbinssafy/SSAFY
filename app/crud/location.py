from sqlalchemy.orm import Session

from app.models.location import Location
from app.schemas.location import LocationCreate, LocationUpdate


def get_locations(db: Session):
    return db.query(Location).order_by(Location.id.desc()).all()


def get_location(db: Session, location_id: int):
    return db.query(Location).filter(Location.id == location_id).first()


def create_location(db: Session, location: LocationCreate):
    db_location = Location(
        name=location.name,
        address=location.address,
        description=location.description,
        category_name=location.category_name,
        image_url=location.image_url,
    )

    db.add(db_location)
    db.commit()
    db.refresh(db_location)

    return db_location


def update_location(db: Session, location_id: int, location: LocationUpdate):
    db_location = db.query(Location).filter(Location.id == location_id).first()

    if db_location is None:
        return None

    db_location.name = location.name
    db_location.address = location.address
    db_location.description = location.description
    db_location.category_name = location.category_name
    db_location.image_url = location.image_url

    db.commit()
    db.refresh(db_location)

    return db_location

def delete_location(db: Session, location_id: int):
    db_location = db.query(Location).filter(Location.id == location_id).first()

    if db_location is None:
        return None

    db.delete(db_location)
    db.commit()

    return db_location