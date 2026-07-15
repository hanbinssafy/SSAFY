from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)

    password = Column(String(20), nullable=False)

    category_id = Column(Integer, ForeignKey("categories.id"))

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    category = relationship("Category", back_populates="posts")