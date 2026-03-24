from pydantic import BaseModel, Field


class TopProductResponse(BaseModel):
    id: int
    name: str
    slug: str
    price: float | None = None
    new_price: float | None = Field(None, alias="newPrice")
    is_in_stock: bool = Field(..., alias="isInStock")
    image_path: str = Field(..., alias='imagePath')

    model_config = {
        "populate_by_name": True,
    }