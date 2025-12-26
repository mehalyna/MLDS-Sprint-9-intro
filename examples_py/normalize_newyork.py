# normalize_newyork.py - New York Weather Data Normalization
import re

def normalize_date(date_str):
    """Normalize date to ISO format"""
    if isinstance(date_str, str):
        if re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
            return date_str
        
        # Handle DD/MM/YYYY format
        if re.match(r'^\d{2}/\d{2}/\d{4}$', date_str):
            # BUG: Assuming MM/DD/YYYY instead of DD/MM/YYYY
            parts = date_str.split('/')
            return f"{parts[2]}-{parts[0]}-{parts[1]}"  # Wrong order!
        
        if 'T' in date_str:
            return date_str.split('T')[0]
    return date_str

def normalize_newyork_data(data):
    """
    Normalize New York weather data (Weather API style)
    Expected structure: location, forecast[{date, temp_max, ...}]
    """
    normalized = []
    city_name = data.get('location', 'New York')
    forecast = data.get('forecast', [])
    
    for item in forecast:
        normalized.append({
            'city': city_name,
            'date': normalize_date(item.get('date')),
            'max': item.get('temp_max'),
            'min': item.get('temp_min'),
            'precip': item.get('precip', 0.0),
            'wind': item.get('wind'),
            'humidity': item.get('humidity')
        })
    
    return normalized