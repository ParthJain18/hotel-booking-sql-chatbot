from pydantic import BaseModel
from datetime import date
from typing import Optional

class HotelBookingBase(BaseModel):
    hotel: str
    is_canceled: bool
    lead_time: int
    stays_in_weekend_nights: int
    stays_in_week_nights: int
    adults: int
    children: Optional[int] = 0
    babies: int = 0
    country: str
    is_repeated_guest: bool
    reserved_room_type: str
    assigned_room_type: str
    booking_changes: int
    days_in_waiting_list: int
    adr: float
    total_of_special_requests: int
    reservation_status: str
    reservation_status_date: date
    revenue: Optional[float] = 0
    check_in_date: Optional[date] = None
    month: Optional[str] = None

class HotelBookingCreate(HotelBookingBase):
    pass

class ChatQuery(BaseModel):
    query: str
    history_id: Optional[int] = None

class HotelBooking(HotelBookingBase):
    id: int
    
    class Config:
        from_attributes = True
        orm_mode = True
