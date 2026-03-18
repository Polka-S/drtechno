from typing import Optional
from sqlalchemy import Numeric, String, ForeignKey, JSON, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from app.core.db import Base


class Product(Base):
    __tablename__ = "products"

    name:             Mapped[str]                    = mapped_column(String(200), nullable=False)
    slug:             Mapped[str]                    = mapped_column(String(220), nullable=False)
    description:      Mapped[Optional[list[str]]]    = mapped_column(JSON)
    features:         Mapped[Optional[dict]]         = mapped_column(JSON) 
    created_at:       Mapped[datetime]               = mapped_column(server_default=func.now())
    updated_at:       Mapped[Optional[datetime]]     = mapped_column(onupdate=func.now())
    category_id:      Mapped[Optional[int]]          = mapped_column(ForeignKey("categories.id"))
    brand_id:         Mapped[Optional[int]]          = mapped_column(ForeignKey("brands.id"))
    
    category:         Mapped[Optional["Category"]]   = relationship(back_populates="products")
    brand:            Mapped[Optional["Brand"]]      = relationship(back_populates="products")
    
    variants:         Mapped[list["ProductVariant"]] = relationship(
        back_populates="product",
        cascade="all, delete-orphan"
    )

    attributes:       Mapped[list["AttributeValue"]] = relationship(
        secondary="product_attributes",
        back_populates="products"
    )

class ProductVariant(Base):
    __tablename__ = "product_variants"

    product_id:       Mapped[int]                 = mapped_column(ForeignKey("products.id"), nullable=False)
    color:            Mapped[Optional[str]]       = mapped_column(String(50))
    normalized_color: Mapped[Optional[str]]       = mapped_column(String(50))
    price:            Mapped[Optional[float]]     = mapped_column(Numeric(10, 2), nullable=True)
    new_price:        Mapped[Optional[float]]     = mapped_column(Numeric(10, 2), nullable=True)
    article:          Mapped[str]                 = mapped_column(String(50), unique=True, nullable=False)
    is_in_stock:      Mapped[bool]                = mapped_column(default=True)
    link:             Mapped[Optional[str]]       = mapped_column(String(500))
    source_id:        Mapped[Optional[str]]       = mapped_column(String(50))

    product:          Mapped["Product"]           = relationship(back_populates="variants")
    accessories:      Mapped[list["ProductVariant"]] = relationship(
        secondary="product_accessories",
        primaryjoin="ProductVariant.id == product_accessories.c.product_variant_id",
        secondaryjoin="ProductVariant.id == product_accessories.c.accessory_variant_id",
        backref="user_as_accessory_for"
    )