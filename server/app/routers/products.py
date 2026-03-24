from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas.product import TopProductResponse
from app.services.product import get_top_products, get_main_image_path_by_product_id


router = APIRouter(
    prefix="/products",
    tags=["products"]
)



@router.get("/top")
def get_top_products_route(limit: int = 10, db: Session = Depends(get_db)):
    products = get_top_products(db, limit)
    result = []
    for product in products:
        images_path = get_main_image_path_by_product_id(db, product.id)
        
        variant = product.variants[0] if product.variants else None
        result.append(TopProductResponse(
            id=product.id,
            name=product.name,
            slug=product.slug,
            price=variant.price if variant.price else None,
            new_price=variant.new_price,
            image_path=images_path,
        ))
    return result