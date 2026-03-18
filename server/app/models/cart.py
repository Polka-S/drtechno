from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime

from app.core.db import Base


class Cart(Base):
    __tablename__ = "carts"

    user_id:              Mapped[int]                = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at:           Mapped[datetime]           = mapped_column(server_default=func.now())
    updated_at:           Mapped[datetime]           = mapped_column(server_default=func.now())

    user:                 Mapped["User"]             = relationship("User", back_populates="cart")
    items:                Mapped[list["CartItem"]]   = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")


class CartItem(Base):
    __tablename__ = "cart_items"

    cart_id:              Mapped[int]                = mapped_column(ForeignKey("carts.id"), nullable=False)
    product_variant_id:   Mapped[int]                = mapped_column(ForeignKey("product_variants.id"), nullable=False)
    quantity:             Mapped[int]                = mapped_column(default=1, nullable=False)

    cart:                 Mapped["Cart"]             = relationship("Cart", back_populates="items")
    product_variant:      Mapped["ProductVariant"]   = relationship()