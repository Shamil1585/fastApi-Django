from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), unique=True, nullable=False)
    email = Column(String(254), unique=True, nullable=False)

    posts = relationship("Post", back_populates="author")
    comments = relationship("Comment", back_populates="author")

    def __repr__(self):
        return f"<User {self.username}>"