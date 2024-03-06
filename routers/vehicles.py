import uuid

from fastapi import APIRouter


router = APIRouter(
    prefix="/vehicles",
    tags=["vehicles"],
)


@router.get("/")
async def get_vehicles():
    return [{"id": uuid.uuid4()}, {"id": uuid.uuid4()}]


@router.get("/{vehicle_id}")
async def get_vehicle(vehicle_id: uuid.UUID) -> dict[str, uuid.UUID]:
    return {"id": vehicle_id}
