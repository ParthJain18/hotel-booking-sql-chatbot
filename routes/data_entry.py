from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
import pandas as pd

from models.database import get_db, HotelBooking

router = APIRouter(prefix="/data-entry", tags=["data-entry"])
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def data_entry_page(request: Request):
    return templates.TemplateResponse("data_entry.html", {"request": request})

@router.post("/")
async def add_booking(
    request: Request,
    db: Session = Depends(get_db),
    
    hotel: str = Form(...),
    lead_time: int = Form(...),
    check_in_date: str = Form(...),
    month: str = Form(...),
    
    stays_in_weekend_nights: int = Form(...),
    stays_in_week_nights: int = Form(...),
    
    adults: int = Form(...),
    children: Optional[int] = Form(0),
    babies: Optional[int] = Form(0),
    country: str = Form(...),
    is_repeated_guest: int = Form(...),
    
    reserved_room_type: str = Form(...),
    assigned_room_type: str = Form(...),
    booking_changes: Optional[int] = Form(0),
    days_in_waiting_list: Optional[int] = Form(0),
    
    adr: float = Form(...),
    total_of_special_requests: Optional[int] = Form(0),
    
    reservation_status: str = Form(...),
    reservation_status_date: str = Form(...)
):
    total_nights = stays_in_weekend_nights + stays_in_week_nights
    revenue = adr * total_nights
    
    check_in_date_obj = datetime.strptime(check_in_date, "%Y-%m-%d").date()
    reservation_status_date_obj = datetime.strptime(reservation_status_date, "%Y-%m-%d").date()
    
    new_booking = HotelBooking(
        hotel=hotel,
        is_canceled=0,
        lead_time=lead_time,
        stays_in_weekend_nights=stays_in_weekend_nights,
        stays_in_week_nights=stays_in_week_nights,
        adults=adults,
        children=children,
        babies=babies,
        country=country,
        is_repeated_guest=is_repeated_guest,
        reserved_room_type=reserved_room_type,
        assigned_room_type=assigned_room_type,
        booking_changes=booking_changes,
        days_in_waiting_list=days_in_waiting_list,
        adr=adr,
        total_of_special_requests=total_of_special_requests,
        reservation_status=reservation_status,
        reservation_status_date=reservation_status_date_obj,
        revenue=revenue,
        check_in_date=check_in_date_obj,
        month=month
    )
    
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    
    return RedirectResponse(url="/data-entry?success=true", status_code=303)