import time

additional_prompt=f"""
    ADDITIONAL INSTRUCTIONS:
    
    1. For revenue calculations, use the 'adr' (average daily rate) column multiplied by the total stay duration (stays_in_weekend_nights + stays_in_week_nights) or the  revenue column that has revenues collected from individual bookings.
    
    2. When calculating occupancy rates or guest counts, remember that adults, children, and babies are all counted separately in the database.
    
    3. For questions about cancellations, use the 'is_canceled' column (1 = canceled, 0 = not canceled).
    
    4. When analyzing seasonal trends, consider the arrival_date_month field for monthly patterns.
    
    5. Lead time refers to the number of days between booking and arrival date.

    6. Current date is {time.strftime("%Y-%m-%d")}.

    7. reservation_status column has three possible values: 'Check-Out', 'Canceled', 'No-Show'.

    8. month column has Dates in the format of 'YYYY-MM-dd'.
    
    Now, please answer the question with a well-formed SQL query.
    
"""