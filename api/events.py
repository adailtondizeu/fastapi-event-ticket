from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def read_events():
    pass

@router.post("/")
def create_event():
    pass

@router.get("/{event_id}")
def read_event(event_id: int):
    pass
