from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def read_tickets():
    pass

@router.post("/")
def create_ticket():
    pass

@router.get("/{ticket_id}")
def read_ticket(ticket_id: int):
    pass