from pydantic import BaseModel


class TopProductResponce(BaseModel):
    id: int
    name: str
    price: int | None
    new_price: int | None
    image_path: str
    