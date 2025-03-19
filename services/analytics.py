from sqlalchemy import func, extract, and_
from sqlalchemy.orm import Session
from models.database import HotelBooking
from datetime import datetime, timedelta

def get_booking_stats(db: Session):
    current_date = datetime.now().date()
    three_months_ago = current_date - timedelta(days=90)
    
    total_bookings_2025 = db.query(HotelBooking).filter(
        extract('year', HotelBooking.check_in_date) == 2025
    ).count()
    
    canceled_bookings_2025 = db.query(HotelBooking).filter(
        and_(
            extract('year', HotelBooking.check_in_date) == 2025,
            HotelBooking.is_canceled == 1
        )
    ).count()
    
    avg_lead_time_recent = db.query(
        func.avg(HotelBooking.lead_time)
    ).filter(
        HotelBooking.check_in_date >= three_months_ago
    ).scalar() or 0
    
    num_countries = db.query(
        func.count(func.distinct(HotelBooking.country))
    ).scalar() or 0
    
    return {
        "total_bookings": total_bookings_2025,
        "canceled_bookings": canceled_bookings_2025,
        "avg_lead_time": round(float(avg_lead_time_recent), 1),
        "num_countries": num_countries
    }

def generate_static_plots(db: Session):
    # Implemented in the notebook for now

    return True