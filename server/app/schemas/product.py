from pydantic import BaseModel


class TopProductResponse(BaseModel):
    id: int
    name: str
    slug: str
    price: int | None
    new_price: int | None
    image_path: str | None
    