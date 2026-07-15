from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.post import PostCreate, PostResponse, PostUpdate
from app.crud.post import (
    create_post,
    get_posts,
    get_post,
    update_post,
    delete_post as delete_post_crud,
)

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/", response_model=list[PostResponse])
def read_posts(
    search: str | None = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    return get_posts(db, search=search, skip=skip, limit=limit)


@router.get("/{post_id}", response_model=PostResponse)
def read_post(post_id: int, db: Session = Depends(get_db)):
    post = get_post(db, post_id)

    if post is None:
        raise HTTPException(status_code=404, detail="게시글이 없습니다.")

    return post


@router.post("/", response_model=PostResponse)
def write_post(post: PostCreate, db: Session = Depends(get_db)):
    return create_post(db, post)


@router.put("/{post_id}", response_model=PostResponse)
def edit_post(post_id: int, post: PostUpdate, db: Session = Depends(get_db)):
    result = update_post(db, post_id, post)

    if result is None:
        raise HTTPException(status_code=404, detail="게시글이 존재하지 않습니다.")

    if result == "password":
        raise HTTPException(status_code=403, detail="비밀번호가 올바르지 않습니다.")

    return result


@router.delete("/{post_id}", response_model=dict)
def remove_post(post_id: int, password: str, db: Session = Depends(get_db)):
    result = delete_post_crud(db, post_id, password)

    if result is None:
        raise HTTPException(status_code=404, detail="게시글이 존재하지 않습니다.")

    if result == "password":
        raise HTTPException(status_code=403, detail="비밀번호가 올바르지 않습니다.")

    return {"message": "게시글이 삭제되었습니다."}