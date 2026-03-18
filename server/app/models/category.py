from typing import Optional
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class Category(Base):
    __tablename__ = "categories"

    name:           Mapped[str]                   = mapped_column(String(100), nullable=False)
    slug:           Mapped[str]                   = mapped_column(String(120), unique=True, nullable=False)
    parent_id:      Mapped[Optional[int]]         = mapped_column(ForeignKey("categories.id"))
    parent:         Mapped[Optional["Category"]]  = relationship(remote_side="Category.id", back_populates="children")
    children:       Mapped[list["Category"]]      = relationship(back_populates="parent")
    products:       Mapped[list["Product"]]       = relationship(back_populates="category")