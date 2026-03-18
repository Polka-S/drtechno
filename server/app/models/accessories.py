from sqlalchemy import Table, Column, Integer, ForeignKey
from app.core.db import Base

product_accessories = Table(
    "product_accessories",
    Base.metadata,
    Column("product_variant_id", Integer, ForeignKey("product_variants.id"), primary_key=True),
    Column("accessory_variant_id", Integer, ForeignKey("product_variants.id"), primary_key=True)
)