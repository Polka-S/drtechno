from typing import Optional
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime

from app.core.db import Base


class User(Base):
    __tablename__ = "users"

    email:             Mapped[str]                              = mapped_column(String(200), unique=True, nullable=False, index=True)
    hashed_password:   Mapped[str]                              = mapped_column(String(200), nullable=False)
    name:              Mapped[Optional[str]]                    = mapped_column(String(100))
    surname:           Mapped[Optional[str]]                    = mapped_column(String(100))
    phone_number:      Mapped[Optional[str]]                    = mapped_column(String(20))
    is_active:         Mapped[bool]                             = mapped_column(default=True)
    is_superuser:      Mapped[bool]                             = mapped_column(default=False)
    created_at:        Mapped[datetime]                         = mapped_column(server_default=func.now())

    cart:              Mapped[Optional["Cart"]]                 = relationship("Cart", back_populates="user", uselist=False)
    orders:            Mapped[list["Order"]]                    = relationship("Order", back_populates="user")
    addresses:         Mapped[list["Address"]]                  = relationship("Address", back_populates="user")
    wishlist_items:    Mapped[Optional[list["WishListItem"]]]   = relationship("WishListItem", back_populates="user")