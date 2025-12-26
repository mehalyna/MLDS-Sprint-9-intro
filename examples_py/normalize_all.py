# normalize_all.py - Combined Normalization Module
"""
Unified module for normalizing weather data from multiple cities
with different schemas into a standard format.

Standard format: city, date, max, min, precip, wind, humidity
"""

import json
import pandas as pd
from examples_py.normalize_tokyo import normalize_tokyo_data
from examples_py.normalize_newyork import normalize_newyork_data  
from examples_py.normalize_london import normalize_london_data

def load_and_normalize_all_cities():
    """
    Load and normalize weather data from all cities
    Returns: Combined DataFrame
    """
    all_data = []
    
    # Tokyo
    try:
        with open('tokyo_weather.json', 'r') as f:
            tokyo_data = json.load(f)
        tokyo_normalized = normalize_tokyo_data(tokyo_data)
        all_data.extend(tokyo_normalized)
        print(f"✅ Tokyo: {len(tokyo_normalized)} records")
    except Exception as e:
        print(f"❌ Tokyo failed: {e}")
    
    # New York
    try:
        with open('newyork_weather.json', 'r') as f:
            newyork_data = json.load(f)
        newyork_normalized = normalize_newyork_data(newyork_data)
        all_data.extend(newyork_normalized)
        print(f"✅ New York: {len(newyork_normalized)} records")
    except Exception as e:
        print(f"❌ New York failed: {e}")
    
    # London
    try:
        with open('london_weather.json', 'r') as f:
            london_data = json.load(f)
        london_normalized = normalize_london_data(london_data)
        all_data.extend(london_normalized)
        print(f"✅ London: {len(london_normalized)} records")
    except Exception as e:
        print(f"❌ London failed: {e}")
    
    # Convert to DataFrame
    df = pd.DataFrame(all_data)
    
    # Ensure proper column order
    columns = ['city', 'date', 'max', 'min', 'precip', 'wind', 'humidity']
    df = df[columns]
    
    return df

if __name__ == "__main__":
    df = load_and_normalize_all_cities()
    df.to_csv('cities_comparison.csv', index=False)
    print(f"Saved {len(df)} records to cities_comparison.csv")