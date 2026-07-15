import json
from pathlib import Path

from app.database import Base, engine, SessionLocal
from app.models.category import Category
from app.models.location import Location
from app.models.post import Post
import app.models

Base.metadata.create_all(bind=engine)

db = SessionLocal()

category_names = [
    "관광지",
    "음식점",
    "축제",
    "숙박",
    "쇼핑",
    "문화시설",
    "레포츠",
    "여행코스",
]

for name in category_names:
    exists = db.query(Category).filter(Category.name == name).first()
    if not exists:
        db.add(Category(name=name))

db.commit()

data_dir = Path(__file__).resolve().parent / "구미_경북권"

source_files = [
    ("관광지", data_dir / "구미_경북권_관광지.json"),
    ("음식점", data_dir / "구미_경북권_음식점.json"),
    ("축제", data_dir / "구미_경북권_축제공연행사.json"),
    ("숙박", data_dir / "구미_경북권_숙박.json"),
    ("쇼핑", data_dir / "구미_경북권_쇼핑.json"),
    ("문화시설", data_dir / "구미_경북권_문화시설.json"),
    ("레포츠", data_dir / "구미_경북권_레포츠.json"),
    ("여행코스", data_dir / "구미_경북권_여행코스.json"),
]

for category_name, file_path in source_files:
    if not file_path.exists():
        continue

    with file_path.open(encoding="utf-8") as f:
        payload = json.load(f)

    content_type = payload.get("contentType") or category_name

    for item in payload.get("items", []):
        title = (item.get("title") or "").strip()
        if not title:
            continue

        address = (item.get("addr1") or "").strip()
        image_url = (item.get("firstimage") or item.get("firstimage2") or "").strip()

        exists = db.query(Location).filter(
            (Location.name == title) | (Location.image_url == image_url)
        ).first()
        if exists:
            continue

        db.add(
            Location(
                name=title,
                address=address or "주소 정보 없음",
                description=f"{content_type} 데이터 기반 장소입니다.",
                category_name=content_type,
                image_url=image_url or None,
            )
        )

db.commit()

category_id_map = {category.name: category.id for category in db.query(Category).all()}

posts = [
    {
        "title": "구미 여행 코스 추천",
        "content": "구미의 관광지와 음식점을 함께 둘러보는 여행 코스입니다.",
        "password": "1234",
        "category_name": "관광지",
    },
    {
        "title": "구미 맛집 후기",
        "content": "구미의 다양한 음식점을 소개하는 포스트입니다.",
        "password": "1234",
        "category_name": "음식점",
    },
    {
        "title": "구미 축제 정보",
        "content": "구미의 축제와 행사 정보를 정리한 포스트입니다.",
        "password": "1234",
        "category_name": "축제",
    },
]

for post_data in posts:
    exists = db.query(Post).filter(Post.title == post_data["title"]).first()
    if not exists:
        db.add(
            Post(
                title=post_data["title"],
                content=post_data["content"],
                password=post_data["password"],
                category_id=category_id_map[post_data["category_name"]],
            )
        )

db.commit()
db.close()

print("구미·경북권 Seed 완료")