from sqlalchemy.orm import Session

from .core.db import SessionLocal
from .logger import setup_logging
from .services import delete_brand, get_top_products

setup_logging()
db: Session = SessionLocal()


if __name__ == "__main__":
    try:
        top_products = get_top_products(db, limit=30)
        for product in top_products:
            print(product)
    finally:
        db.close()


    