from typing import Optional
from sqlalchemy import Numeric, String, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime

from app.core.db import Base


class WishListItem(Base):
    __tablename__ = "wishlist_items"

    user_id:               Mapped[int]                = mapped_column(ForeignKey("users.id"), nullable=False)
    product_variant_id:    Mapped[int]                = mapped_column(ForeignKey("product_variants.id"), nullable=False)
    
    user:                  Mapped["User"]             = relationship(back_populates="wishlist_items")
    product_variant:       Mapped["ProductVariant"]   = relationship()