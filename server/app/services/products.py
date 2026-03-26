import os
import logging
from sqlalchemy.orm import Session
from sqlalchemy import func, select
from pathlib import Path

from app.models import (
    Product,
    ProductVariant,
    product_accessories
)


logger = logging.getLogger(__name__)


def get_images_dir_by_product_id(db: Session, product_id: int) -> str:
    """
    Возвращает путь к изображениям для заданного продукта.
    """

    try:
        query = (
            select(ProductVariant.source_id).where(ProductVariant.product_id == product_id)
        )    
        result = db.execute(query).scalars().first()
        return result
    except Exception as e:
        logger.error(f"Error fetching images for product {product_id}: {e}")
        return []


def get_main_image_path_by_product_id(db: Session, product_id: int) -> str:
    """
    Возвращает путь к главному изображению для заданного продукта.
    """
    
    product_dir = get_images_dir_by_product_id(db, product_id)
    path = Path(f"../client/public/products/{product_dir}")

    try:
        matches = list(path.glob("1.*"))
        if not matches:
            print("pizdec", matches)
            return None
        return f"/products/{product_dir}/{matches[0].name}"
    except Exception as e:
        logger.error(f"Error fetching main image for product {product_id}: {e}")
        return []


def get_top_products(db: Session, limit: int = 10) -> list[Product]:
    """
    Возвращает топ продуктов по количеству аксессуаров.
    """
    try:
        subq = (
            select(
                product_accessories.c.product_variant_id,
                func.count().label('accessory_count')
            )
            .group_by(product_accessories.c.product_variant_id)
            .subquery()
        )

        query = (
            select(Product)
            .join(ProductVariant, ProductVariant.product_id == Product.id)
            .outerjoin(subq, ProductVariant.id == subq.c.product_variant_id)
            .group_by(Product.id)
            .order_by(func.coalesce(func.sum(subq.c.accessory_count), 0).desc())
            .limit(limit)
        )

        products = db.execute(query).scalars().all()
        logger.info(f"Retrieved top {len(products)} products.")
        return products
    except Exception as e:
        logger.error(f"Error in get_top_products: {e}")
        return []