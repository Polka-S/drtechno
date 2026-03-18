from typing import Optional
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class Address(Base):
    __tablename__ = "addresses"

    user_id:       Mapped[int]                = mapped_column(ForeignKey("users.id"), nullable=False)
    name:          Mapped[str]                = mapped_column(String(255))
    phone:         Mapped[str]                = mapped_column(String(20))
    country:       Mapped[str]                = mapped_column(String(100), nullable=False)
    city:          Mapped[str]                = mapped_column(String(100), nullable=False)
    street:        Mapped[str]                = mapped_column(String(200), nullable=False)
    house:         Mapped[str]                = mapped_column(String(20))
    apartment:     Mapped[Optional[str]]      = mapped_column(String(20))
    postal_code:   Mapped[Optional[str]]      = mapped_column(String(20))
    is_default:    Mapped[bool]               = mapped_column(default=False)

    user:          Mapped["User"]             = relationship(back_populates="addresses")
    orders:        Mapped[list["Order"]]      = relationship(back_populates="address")