from .products import router as products_router
from .brands import router as brands_router
from .auth import router as auth_router


routers = [
    products_router,
    brands_router,
    auth_router,
]