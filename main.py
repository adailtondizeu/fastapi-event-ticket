from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from databases import Database


DATABASE_URL = "sqlite:///./ticket_sales.db"
database = Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)

    tickets = relationship("Ticket", back_populates="event")


class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    ticket_type = Column(String)
    quantity = Column(Integer)

    event = relationship("Event", back_populates="tickets")


Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}


@app.post("/events/", status_code=201)
async def create_event(name: str, description: str, price: float):
    query = Event(name=name, description=description, price=price)
    database.execute(query)
    return {"name": name, "description": description, "price": price}


@app.get("/events/")
async def get_events():
    query = Event.__table__.select()
    return await database.fetch_all(query)


@app.get("/events/{event_id}")
async def get_event(event_id: int):
    query = Event.__table__.select().where(Event.id == event_id)
    event = await database.fetch_one(query)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@app.post("/events/{event_id}/buy/", status_code=201)
async def buy_ticket(event_id: int, ticket_type: str, quantity: int):
    event_query = Event.__table__.select().where(Event.id == event_id)
    event = await database.fetch_one(event_query)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    ticket = Ticket(event_id=event_id, ticket_type=ticket_type, quantity=quantity)
    database.execute(ticket)
    return {"event": event, "ticket_type": ticket_type, "quantity": quantity}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
