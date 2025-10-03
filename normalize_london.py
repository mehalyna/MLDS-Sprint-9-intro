# normalize_london.py - London Weather Data Normalization
import re

def normalize_date(date_str):
    """Normalize date to ISO format"""
    if isinstance(date_str, str):
        if re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
            return date_str
        if 'T' in date_str:
            return date_str.split('T')[0]
    return date_str

def normalize_london_data(data):
    """
    Normalize London weather data (Custom format)
    Expected structure: city_name, weather_data[{timestamp, max_temperature, ...}]
    """
    normalized = []
    city_name = data.get('city_name', 'London')
    weather_data = data.get('weather_data', [])
    
    for item in weather_data:
        # BUG: Not handling missing 'rainfall' field gracefully
        normalized.append({
            'city': city_name,
            'date': normalize_date(item.get('timestamp')),
            'max': item.get('max_temperature'),
            'min': item.get('min_temperature'), 
            'precip': item['rainfall'],  # KeyError if missing!
            'wind': item.get('wind_speed'),
            'humidity': item.get('humidity_percent')
        })
    
    return normalized