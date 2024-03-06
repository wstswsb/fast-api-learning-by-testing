import uuid

from fastapi import APIRouter


router = APIRouter(
    prefix="/presentations",
    tags=["presentations"],
)


@router.get("/")
async def get_presentations():
    return [{"id": uuid.uuid4()}, {"id": uuid.uuid4()}]


@router.get("/{presentation_id}")
async def get_presentation(presentation_id: uuid.UUID) -> dict[str, uuid.UUID]:
    return {"id": presentation_id}
