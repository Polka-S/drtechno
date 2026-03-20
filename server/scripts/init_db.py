from sqlalchemy import inspect

from app.core.db import engine, Base
from app.models import (
    Category,
    Brand,
    Product,
    ProductVariant,
    Attribute,
    AttributeValue,
    product_accessories,
)


print("Creating database tables...")

Base.metadata.create_all(bind=engine)

print("Database tables created successfully.")