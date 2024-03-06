__all__ = [
    "documents_router",
    "presentations_router",
    "vehicles_router",
]

from routers.documents import router as documents_router
from routers.presentations import router as presentations_router
from routers.vehicles import router as vehicles_router
