from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    is_published = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    title = Column(String(256), nullable=False)
    description = Column(Text, nullable=False)
    slug = Column(String(256), unique=True, nullable=False, index=True)

    posts = relationship("Post", back_populates="category")

    def __repr__(self):
        return f"<Category {self.title}>"