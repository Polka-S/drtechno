from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Table, UniqueConstraint
from typing import List

from app.core.db import Base


class Attribute(Base):
    __tablename__ = "attributes"

    name:           Mapped[str]                     = mapped_column(String(100), unique=True, nullable=False)
    slug:           Mapped[str]                     = mapped_column(String(120), unique=True, nullable=False)
    values:         Mapped[list["AttributeValue"]]  = relationship(back_populates="attribute")


class AttributeValue(Base):
    __tablename__ = "attribute_values"

    attribute_id:   Mapped[int]                     = mapped_column(ForeignKey("attributes.id"))
    value:          Mapped[str]                     = mapped_column(String(200), nullable=False)
    attribute:      Mapped["Attribute"]             = relationship(back_populates="values")
    products:       Mapped[List["Product"]]         = relationship(
        secondary="product_attributes",
        back_populates="attributes"
    )

    __table_args__ = (UniqueConstraint('attribute_id', 'value', name='_attribute_value_uc'),)

product_attributes = Table(
    "product_attributes",
    Base.metadata,
    Column("product_id", Integer, ForeignKey("products.id"), primary_key=True),
    Column("attribute_value_id", Integer, ForeignKey("attribute_values.id"), primary_key=True)
)