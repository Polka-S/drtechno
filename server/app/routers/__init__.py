from .products import router as products_router
from .brands import router as brands_router


routers = [
    products_router,
    brands_router,
]