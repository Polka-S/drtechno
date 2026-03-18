from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

from app.core.db import Base


class Brand(Base):
    __tablename__ = "brands"

    name:          Mapped[str]                = mapped_column(String(100), unique=True, nullable=False)
    slug:          Mapped[str]                = mapped_column(String(120), unique=True, nullable=False)
    
    products:      Mapped[list["Product"]]    = relationship(back_populates="brand")