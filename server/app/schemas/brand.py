from pydantic import BaseModel


class BrandBase(BaseModel):
    id: int
    name: str
    slug: str