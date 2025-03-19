import pandas as pd
import matplotlib.pyplot as plt
import os
from sqlalchemy import func
from sqlalchemy.orm import Session
from models.database import HotelBooking

def get_booking_stats(db: Session):
    total_bookings = db.query(HotelBooking).count()
    active_bookings = db.query(HotelBooking).filter(HotelBooking.is_canceled == 0).count()
    canceled_bookings = db.query(HotelBooking).filter(HotelBooking.is_canceled == 1).count()
    avg_lead_time = db.query(func.avg(HotelBooking.lead_time)).scalar() or 0
    
    return {
        "total_bookings": total_bookings,
        "active_bookings": active_bookings,
        "canceled_bookings": canceled_bookings,
        "avg_lead_time": round(float(avg_lead_time), 1)
    }

def generate_static_plots(db: Session):
    """Generate all the static plots and save them to the static/plots directory"""
    # Create the plots directory if it doesn't exist
    os.makedirs("static/plots", exist_ok=True)
    
    # Convert SQLAlchemy query to pandas DataFrame for easier manipulation
    query = db.query(HotelBooking).all()
    df = pd.DataFrame([{c.name: getattr(obj, c.name) for c in obj.__table__.columns} for obj in query])
    
    # Chart 1: Bookings by hotel type
    plt.figure(figsize=(10, 6))
    hotel_counts = df.groupby('hotel').size()
    hotel_counts.plot(kind='pie', autopct='%1.1f%%')
    plt.title('Bookings by Hotel Type')
    plt.savefig('static/plots/hotel_types.png', bbox_inches='tight')
    plt.close()
    
    # Chart 2: Cancellation rate by month
    plt.figure(figsize=(10, 6))
    df['month'] = pd.to_datetime(df['arrival_date']).dt.month_name()
    cancellation_by_month = pd.crosstab(df['month'], df['is_canceled'])
    cancellation_by_month.plot(kind='bar', stacked=True)
    plt.title('Cancellation Rate by Month')
    plt.xlabel('Month')
    plt.ylabel('Number of Bookings')
    plt.legend(['Not Canceled', 'Canceled'])
    plt.savefig('static/plots/cancellation_rate.png', bbox_inches='tight')
    plt.close()
    
    # Chart 3: Distribution of room types
    plt.figure(figsize=(10, 6))
    room_type_counts = df.groupby('reserved_room_type').size()
    room_type_counts.plot(kind='pie', autopct='%1.1f%%')
    plt.title('Room Type Distribution')
    plt.savefig('static/plots/room_types.png', bbox_inches='tight')
    plt.close()
    
    # Chart 4: Average daily rate by market segment
    plt.figure(figsize=(10, 6))
    adr_by_market = df.groupby('market_segment')['adr'].mean()
    adr_by_market.plot(kind='bar')
    plt.title('ADR by Market Segment')
    plt.xlabel('Market Segment')
    plt.ylabel('Average Daily Rate')
    plt.savefig('static/plots/adr_market.png', bbox_inches='tight')
    plt.close()
    
    # Chart 5: Distribution of customer types
    plt.figure(figsize=(10, 6))
    customer_type_counts = df.groupby('customer_type').size()
    customer_type_counts.plot(kind='pie', autopct='%1.1f%%')
    plt.title('Customer Type Distribution')
    plt.savefig('static/plots/customer_types.png', bbox_inches='tight')
    plt.close()
    
    # Chart 6: Average stay length by hotel type
    plt.figure(figsize=(10, 6))
    df['total_stay'] = df['stays_in_weekend_nights'] + df['stays_in_week_nights']
    stay_length_stats = df.groupby('hotel')['total_stay'].mean()
    stay_length_stats.plot(kind='bar')
    plt.title('Average Stay Length by Hotel Type')
    plt.xlabel('Hotel Type')
    plt.ylabel('Average Stay Length (Days)')
    plt.savefig('static/plots/stay_length.png', bbox_inches='tight')
    plt.close()

    return True