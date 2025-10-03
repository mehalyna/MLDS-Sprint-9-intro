# normalize_tokyo.py - Tokyo Weather Data Normalization
import re

def normalize_date(date_str):
    """Normalize date to ISO format"""
    if isinstance(date_str, str):
        if re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
            return date_str
        if 'T' in date_str:
            return date_str.split('T')[0]
    return date_str

def normalize_tokyo_data(data):
    """
    Normalize Tokyo weather data (Open-Meteo style)
    Expected structure: daily.time, daily.temperature_2m_max, etc.
    """
    normalized = []
    daily = data.get('daily', {})
    
    dates = daily.get('time', [])
    max_temps = daily.get('temperature_2m_max', [])
    min_temps = daily.get('temperature_2m_min', [])
    precip = daily.get('precipitation_sum', [])
    wind = daily.get('windspeed_10m_max', [])
    humidity = daily.get('relative_humidity_2m', [])
    
    # BUG: Not validating array lengths
    for i in range(len(dates)):
        normalized.append({
            'city': 'Tokyo',
            'date': normalize_date(dates[i]),
            'max': max_temps[i] if i < len(max_temps) else None,
            'min': min_temps[i] if i < len(min_temps) else None,
            'precip': precip[i] if i < len(precip) else 0.0,
            'wind': wind[i] if i < len(wind) else None,
            'humidity': humidity[i] if i < len(humidity) else None
        })
    
    return normalized