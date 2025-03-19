from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional

from models.database import get_db, HotelBooking
from models.schemas import HotelBookingCreate

router = APIRouter(prefix="/data-entry", tags=["data-entry"])
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def data_entry_page(request: Request):
    return templates.TemplateResponse("data_entry.html", {"request": request})

@router.post("/")
async def add_booking(
    request: Request,
    db: Session = Depends(get_db),
    # Add all form fields here with Form dependency
    hotel: str = Form(...),
    is_canceled: bool = Form(...),
    # ... add other fields
):
    # Create new booking object
    new_booking = HotelBooking(
        hotel=hotel,
        is_canceled=is_canceled,
        # ... add other fields
    )
    db.add(new_booking)
    db.commit()
    
    return RedirectResponse(url="/data-entry?success=true", status_code=303)