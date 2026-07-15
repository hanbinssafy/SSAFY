from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate

from datetime import datetime


def create_post(db: Session, post: PostCreate):
    db_post = Post(
        title=post.title,
        content=post.content,
        password=post.password,
        category_id=post.category_id,
    )

    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    return db_post


def get_posts(db: Session, search: str | None = None, skip: int = 0, limit: int = 10):
    query = db.query(Post)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Post.title.ilike(search_term),
                Post.content.ilike(search_term),
            )
        )

    return query.order_by(Post.id.desc()).offset(skip).limit(limit).all()


def get_post(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()


def update_post(db: Session, post_id: int, post: PostUpdate):
    db_post = db.query(Post).filter(Post.id == post_id).first()

    if db_post is None:
        return None

    if db_post.password != post.password:
        return "password"

    db_post.title = post.title
    db_post.content = post.content
    db_post.category_id = post.category_id
    db_post.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(db_post)

    return db_post


def delete_post(db: Session, post_id: int, password: str):
    db_post = db.query(Post).filter(Post.id == post_id).first()

    if db_post is None:
        return None

    if db_post.password != password:
        return "password"

    db.delete(db_post)
    db.commit()

    return db_post