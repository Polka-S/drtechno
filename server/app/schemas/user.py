from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserBase(BaseModel):
    id: int
    email: EmailStr
    name: str
    is_superuser: bool = Field(..., alias='isSuperuser')
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str
    phone_number: str | None = None