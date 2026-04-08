import logging
from sqlalchemy.orm import Session
from sqlalchemy import func, select

from app.models import Brand


logger = logging.getLogger(__name__)

def delete_brand(brand_name: str, db: Session) -> None:
    """
    Удаляет бренд по имени.
    """

    brand = db.query(Brand).filter_by(name = brand_name).first()
    
    if brand: 
        db.delete(brand)
        db.commit()
        
        logger.warning(f"Brand '{brand_name}' has been deleted.")
    else:
        logger.warning(f"Brand '{brand_name}' not found.")

def get_brands(db: Session) -> list[Brand]:
    """
    Возвращает все бренды.
    """
    
    return db.query(Brand).all()