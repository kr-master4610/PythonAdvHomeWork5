from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)

    questions = relationship("Question", back_populates="category", cascade="all, delete-orphan")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(255), nullable=False)
    answer = Column(String(255), nullable=False)

    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("Category", back_populates="questions")