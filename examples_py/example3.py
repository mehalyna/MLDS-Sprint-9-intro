# Task C - Normalize & Combine Weather Files Implementation
import json
import pandas as pd
import os
from datetime import datetime, timedelta
import re

def create_sample_weather_data():
    """
    Create sample JSON files for three cities with different schemas
    """
    # Tokyo data - Schema 1: Open-Meteo style
    tokyo_data = {
        "city": "Tokyo",
        "daily": {
            "time": ["2024-08-18", "2024-08-19", "2024-08-20"],
            "temperature_2m_max": [32.5, 31.8, 33.2],
            "temperature_2m_min": [22.5, 21.9, 23.1],
            "precipitation_sum": [0.0, 2.5, 0.0],
            "windspeed_10m_max": [15.5, 18.2, 12.8],
            "relative_humidity_2m": [65, 72, 68]
        }
    }
    
    # New York data - Schema 2: Weather API style  
    newyork_data = {
        "location": "New York",
        "forecast": [
            {
                "date": "18/08/2024",  # Different date format
                "temp_max": 28.3,
                "temp_min": 18.7,
                "precip": 1.2,
                "wind": 22.5,
                "humidity": 58
            },
            {
                "date": "19/08/2024",
                "temp_max": 29.1,
                "temp_min": 19.4,
                "precip": 0.0,
                "wind": 19.8,
                "humidity": 61
            },
            {
                "date": "20/08/2024",
                "temp_max": 27.8,
                "temp_min": 17.9,
                "precip": 3.1,
                "wind": 25.2,
                "humidity": 64
            }
        ]
    }
    
    # London data - Schema 3: Custom format
    london_data = {
        "city_name": "London",
        "weather_data": [
            {
                "timestamp": "2024-08-18T00:00:00Z",
                "max_temperature": 24.1,
                "min_temperature": 15.3,
                "rainfall": 0.8,
                "wind_speed": 28.5,
                "humidity_percent": 78
            },
            {
                "timestamp": "2024-08-19T00:00:00Z", 
                "max_temperature": 23.5,
                "min_temperature": 14.8,
                "rainfall": 2.3,
                "wind_speed": 31.2,
                "humidity_percent": 82
            },
            {
                "timestamp": "2024-08-20T00:00:00Z",
                "max_temperature": 25.7,
                "min_temperature": 16.1,
                # Missing rainfall data intentionally
                "wind_speed": 26.8,
                "humidity_percent": 75
            }
        ]
    }
    
    # Save sample data files
    with open('tokyo_weather.json', 'w') as f:
        json.dump(tokyo_data, f, indent=2)
    
    with open('newyork_weather.json', 'w') as f:
        json.dump(newyork_data, f, indent=2)
    
    with open('london_weather.json', 'w') as f:
        json.dump(london_data, f, indent=2)
    
    print("Sample weather data files created:")
    print("   - tokyo_weather.json")
    print("   - newyork_weather.json") 
    print("   - london_weather.json")

def normalize_date(date_str):
    """
    Normalize different date formats to ISO YYYY-MM-DD
    BUG: Contains intentional bugs for educational purposes
    """
    # BUG 1: Not handling all possible date formats robustly
    if isinstance(date_str, str):
        # Handle ISO format (already correct)
        if re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
            return date_str
        
        # Handle DD/MM/YYYY format
        if re.match(r'^\d{2}/\d{2}/\d{4}$', date_str):
            # BUG 2: Assuming MM/DD/YYYY instead of DD/MM/YYYY
            parts = date_str.split('/')
            return f"{parts[2]}-{parts[0]}-{parts[1]}"  # Wrong order!
        
        # Handle ISO timestamp
        if 'T' in date_str:
            return date_str.split('T')[0]
    
    # BUG 3: Not handling invalid dates gracefully
    return date_str  # Should validate and possibly raise error

def normalize_tokyo_data(data):
    """
    Normalize Tokyo weather data (Open-Meteo style)
    """
    normalized = []
    daily = data.get('daily', {})
    
    dates = daily.get('time', [])
    max_temps = daily.get('temperature_2m_max', [])
    min_temps = daily.get('temperature_2m_min', [])
    precip = daily.get('precipitation_sum', [])
    wind = daily.get('windspeed_10m_max', [])
    humidity = daily.get('relative_humidity_2m', [])
    
    # BUG 4: Not validating array lengths are equal
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

def normalize_newyork_data(data):
    """
    Normalize New York weather data (Weather API style)
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

def normalize_london_data(data):
    """
    Normalize London weather data (Custom format)
    """
    normalized = []
    city_name = data.get('city_name', 'London')
    weather_data = data.get('weather_data', [])
    
    for item in weather_data:
        # BUG 5: Not handling missing 'rainfall' field gracefully
        normalized.append({
            'city': city_name,
            'date': normalize_date(item.get('timestamp')),
            'max': item.get('max_temperature'),
            'min': item.get('min_temperature'), 
            'precip': item['rainfall'],  # This will cause KeyError if missing!
            'wind': item.get('wind_speed'),
            'humidity': item.get('humidity_percent')
        })
    
    return normalized

def combine_normalized_data(normalized_data_list):
    """
    Combine normalized data from multiple cities into single structure
    """
    combined = []
    for city_data in normalized_data_list:
        combined.extend(city_data)
    
    # BUG 6: Not sorting by date for better organization
    return combined

def save_to_csv(data, filename='cities_comparison.csv'):
    """
    Save combined data to CSV file
    """
    df = pd.DataFrame(data)
    
    # Ensure proper column order
    columns = ['city', 'date', 'max', 'min', 'precip', 'wind', 'humidity']
    df = df[columns]
    
    df.to_csv(filename, index=False)
    print(f"Combined data saved to {filename}")
    return df

def main_normalization():
    """
    Main function to run the complete normalization process
    """
    print("=== Task C: Normalize & Combine Weather Files ===")
    
    # Create sample data
    create_sample_weather_data()
    
    # Load and normalize each city's data
    print("\n Loading and normalizing data...")
    
    # Tokyo
    with open('tokyo_weather.json', 'r') as f:
        tokyo_data = json.load(f)
    tokyo_normalized = normalize_tokyo_data(tokyo_data)
    print(f"   Tokyo: {len(tokyo_normalized)} records")
    
    # New York  
    with open('newyork_weather.json', 'r') as f:
        newyork_data = json.load(f)
    newyork_normalized = normalize_newyork_data(newyork_data)
    print(f"   New York: {len(newyork_normalized)} records")
    
    # London
    with open('london_weather.json', 'r') as f:
        london_data = json.load(f)
    
    try:
        london_normalized = normalize_london_data(london_data)
        print(f"   London: {len(london_normalized)} records")
    except KeyError as e:
        print(f"   London: Error - {e}")
        # Create partial data for London (bug demonstration)
        london_normalized = []
        for item in london_data.get('weather_data', []):
            if 'rainfall' in item:
                london_normalized.append({
                    'city': 'London',
                    'date': normalize_date(item.get('timestamp')),
                    'max': item.get('max_temperature'),
                    'min': item.get('min_temperature'),
                    'precip': item.get('rainfall'),
                    'wind': item.get('wind_speed'),
                    'humidity': item.get('humidity_percent')
                })
        print(f"   London: {len(london_normalized)} records (partial due to missing data)")
    
    # Combine all data
    print("\n Combining normalized data...")
    combined_data = combine_normalized_data([
        tokyo_normalized,
        newyork_normalized, 
        london_normalized
    ])
    
    print(f"   Total records: {len(combined_data)}")
    
    # Save to CSV
    df = save_to_csv(combined_data)
    
    return df

# Run the main process
if __name__ == "__main__":
    result_df = main_normalization()


# Demo Cell - Run Normalization and Show First CSV Row (Run-and-paste check)
print("=== TASK C DEMO OUTPUT ===")

# Run the main normalization process
result_df = main_normalization()

if result_df is not None and len(result_df) > 0:
    print(f"\n📊 REQUESTED VALUE FOR COPY-PASTE:")
    print("First CSV row:")
    first_row = result_df.iloc[0]
    row_string = f"{first_row['city']},{first_row['date']},{first_row['max']},{first_row['min']},{first_row['precip']},{first_row['wind']},{first_row['humidity']}"
    print(row_string)
    
    print(f"\n📄 Full cities_comparison.csv preview (first 5 rows):")
    print(result_df.head().to_string(index=False))
    
    print(f"\n📈 Summary:")
    print(f"   Total cities: {result_df['city'].nunique()}")
    print(f"   Total records: {len(result_df)}")
    print(f"   Date range: {result_df['date'].min()} to {result_df['date'].max()}")
    
else:
    print(" No data generated!")

print("\n=== END DEMO OUTPUT ===")
