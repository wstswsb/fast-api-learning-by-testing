import uuid

from fastapi import APIRouter


router = APIRouter(
    prefix="/documents",
    tags=["documents"],
)


@router.get("/")
async def get_documents():
    return [{"id": uuid.uuid4()}, {"id": uuid.uuid4()}]


@router.get("/{doc_id}")
async def get_document(doc_id: uuid.UUID) -> dict[str, uuid.UUID]:
    return {"id": doc_id}
