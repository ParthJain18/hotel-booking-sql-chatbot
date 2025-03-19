import os
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = "sqlite:///./hotel_bookings.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class HotelBooking(Base):
    __tablename__ = "hotel_bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    hotel = Column(String)
    is_canceled = Column(Boolean)
    lead_time = Column(Integer)
    stays_in_weekend_nights = Column(Integer)
    stays_in_week_nights = Column(Integer)
    adults = Column(Integer)
    children = Column(Integer)
    babies = Column(Integer)
    country = Column(String)
    is_repeated_guest = Column(Boolean)
    reserved_room_type = Column(String)
    assigned_room_type = Column(String)
    booking_changes = Column(Integer)
    days_in_waiting_list = Column(Integer)
    adr = Column(Float)
    total_of_special_requests = Column(Integer)
    reservation_status = Column(String)
    reservation_status_date = Column(Date)
    revenue = Column(Float)
    check_in_date = Column(Date)
    month = Column(String)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_db_and_tables():
    Base.metadata.create_all(bind=engine)
    
    # Import data from CSV if database is empty
    db = SessionLocal()
    if db.query(HotelBooking).count() == 0:
        csv_file = os.path.join("data", "hotel_data.csv")
        if os.path.exists(csv_file):
            df = pd.read_csv(csv_file)
            
            # Handle date columns
            date_columns = ['reservation_status_date', 'check_in_date']
            for col in date_columns:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col]).dt.date
            
            # Convert dataframe to dict and insert to database
            for _, row in df.iterrows():
                row_dict = row.to_dict()
                # Filter to include only columns in our model
                model_columns = set(HotelBooking.__table__.columns.keys()) - {'id'}
                filtered_dict = {k: v for k, v in row_dict.items() if k in model_columns}
                
                db_row = HotelBooking(**filtered_dict)
                db.add(db_row)
            
            db.commit()
    db.close()

if __name__ == "__main__":
    create_db_and_tables()