import sys, os

sys.path.insert(0, os.getcwd())

from fastapi import FastAPI

from app.logger import setup_logging
from app.routers import (
    products_router,
    brands_router,
    auth_router,
)


setup_logging()

app = FastAPI()

app.include_router(products_router)
app.include_router(brands_router)
app.include_router(auth_router)



    