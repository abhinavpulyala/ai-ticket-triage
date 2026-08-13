from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.models import TicketClassification, TicketRequest
from app.triage import classify_ticket

app = FastAPI(
    title="AI Ticket Triage",
    description="Classifies support tickets by department, priority, tags, and response guidance.",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/", include_in_schema=False)
def home() -> FileResponse:
    return FileResponse("app/static/index.html")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/classify", response_model=TicketClassification)
def classify(ticket: TicketRequest) -> TicketClassification:
    return classify_ticket(ticket)
