from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas import BrandBase
from app.services.brands import get_brands


router = APIRouter(
    prefix="/brands",
    tags=["brands"]
)


@router.get("", response_model=list[BrandBase])
def get_brands_route(db: Session = Depends(get_db)) -> list[BrandBase]:
    brands = get_brands(db)
    result = []

    for brand in brands:
        result.append(BrandBase(
            id=brand.id,
            name=brand.name,
            slug=brand.slug,
        ))
    
    return result