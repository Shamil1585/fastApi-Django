from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    is_published = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    title = Column(String(256), nullable=False)
    text = Column(Text, nullable=False)
    pub_date = Column(DateTime(timezone=True), nullable=False)
    image = Column(String(256), nullable=True)

    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    author = relationship("User", back_populates="posts")
    location = relationship("Location", back_populates="posts")
    category = relationship("Category", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Post {self.title}>"