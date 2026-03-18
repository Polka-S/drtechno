from typing import Optional
from sqlalchemy import Numeric, String, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime
from enum import StrEnum

from app.core.db import Base


class OrderStatus(StrEnum):
    PENDING    = "pending"
    PAID       = "paid"
    PROCESSING = "processing"
    SHIPPED    = "shipped"
    DELIVERED  = "delivered"
    CANCELED   = "canceled"

class PaymentStatus(StrEnum):
    PENDING    = "pending"
    PAID       = "paid"
    FAILED     = "failed"
    REFUNDED   = "refunded"


class Order(Base):
    __tablename__ = "orders"

    user_id:             Mapped[int]                           = mapped_column(ForeignKey("users.id"), nullable=False)
    status:              Mapped[OrderStatus]                   = mapped_column(Enum(OrderStatus), default=OrderStatus.PENDING)
    total_amount:        Mapped[float]                         = mapped_column(Numeric(10, 2), nullable=False)
    address_id:          Mapped[Optional[int]]                 = mapped_column(ForeignKey("addresses.id"))
    payment_method:      Mapped[Optional[str]]                 = mapped_column(String(50))
    payment_status:      Mapped[Optional[PaymentStatus]]       = mapped_column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    created_at:          Mapped[datetime]                      = mapped_column(server_default=func.now())
    updated_at:          Mapped[datetime]                      = mapped_column(server_default=func.now())

    user:                Mapped["User"]                        = relationship(back_populates="orders")
    items:               Mapped[list["OrderItem"]]             = relationship(back_populates="order", cascade="all, delete-orphan")
    address:             Mapped[Optional["Address"]]           = relationship()

class OrderItem(Base):
    __tablename__ = "order_items"

    order_id:            Mapped[int]                = mapped_column(ForeignKey("orders.id"), nullable=False)
    product_variant_id:  Mapped[int]                = mapped_column(ForeignKey("product_variants.id"))
    product_name:        Mapped[str]                = mapped_column(String(200), nullable=False)
    variant_color:       Mapped[Optional[str]]      = mapped_column(String(50))
    price:               Mapped[float]              = mapped_column(Numeric(10, 2), nullable=False)
    quantity:            Mapped[int]                = mapped_column(default=1, nullable=False)
    created_at:          Mapped[datetime]           = mapped_column(server_default=func.now())
    
    order:               Mapped["Order"]            = relationship(back_populates="items")
    product_variant:     Mapped["ProductVariant"]   = relationship()