import logging
from sqlalchemy.orm import Session
from sqlalchemy import func, select

from app.models import (
    Product,
    ProductVariant,
    product_accessories
)


logger = logging.getLogger(__name__)

def get_top_products(db: Session, limit: int = 10):
    """Возвращает топ продуктов по количеству аксессуаров."""
    
    try:
        variant_counts = (
            select(
                product_accessories.c.product_variant_id,
                func.count().label('accessory_count')
            )
            .group_by(product_accessories.c.product_variant_id)
            .subquery()
        )
        query = (
            select(
                Product.id,
                Product.name,
                func.coalesce(func.sum(variant_counts.c.accessory_count), 0).label('total_accessories')
            )
            .join(ProductVariant, ProductVariant.product_id == Product.id)
            .outerjoin(variant_counts, ProductVariant.id == variant_counts.c.product_variant_id)
            .group_by(Product.id, Product.name)
            .order_by(func.coalesce(func.sum(variant_counts.c.accessory_count), 0).desc())
            .limit(limit)
        )

        results = db.execute(query).all()
        logger.info(f"Retrieved top {len(results)} products.")
        
        return results
  
    except Exception as e:
        logger.error(f"Error fetching top products: {e}")
        return []