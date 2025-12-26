# Task E - Parse Hourly Weather from XML (BUGGY VERSION)
import xml.etree.ElementTree as ET
import json
import pandas as pd
from datetime import datetime
import re

def create_sample_xml_data():
    """Create sample XML file with hourly weather data including namespaces"""
    xml_content = '''<?xml version="1.0" encoding="UTF-8"?>
<weather xmlns:w="http://weather.example.com/schema" xmlns="http://weather.example.com/default">
    <day date="2024-08-18">
        <hour time="00:00">
            <w:temp>22.1</w:temp>
            <w:wind>12.5</w:wind>
        </hour>
        <hour time="03:00">
            <w:temp>21.8</w:temp>
            <w:wind>13.2</w:wind>
        </hour>
        <hour time="06:00">
            <w:temp>24.5</w:temp>
            <w:wind>15.8</w:wind>
        </hour>
        <hour time="09:00">
            <w:temp>28.3</w:temp>
            <w:wind>18.1</w:wind>
        </hour>
        <hour time="12:00">
            <w:temp>32.1</w:temp>
            <w:wind>20.3</w:wind>
        </hour>
        <hour time="15:00">
            <w:temp>34.2</w:temp>
            <w:wind>22.7</w:wind>
        </hour>
        <hour time="18:00">
            <w:temp>31.5</w:temp>
            <w:wind>19.4</w:wind>
        </hour>
        <hour time="21:00">
            <w:temp>26.8</w:temp>
            <w:wind>16.2</w:wind>
        </hour>
    </day>
    <day date="2024-08-19">
        <hour time="00:00">
            <w:temp>23.4</w:temp>
            <w:wind>14.1</w:wind>
        </hour>
        <hour time="06:00">
            <w:temp>25.2</w:temp>
            <w:wind>16.5</w:wind>
        </hour>
        <hour time="12:00">
            <w:temp>33.8</w:temp>
            <w:wind>21.9</w:wind>
        </hour>
        <hour time="18:00">
            <w:temp>30.1</w:temp>
            <w:wind>18.7</w:wind>
        </hour>
    </day>
    <day date="2024-08-20">
        <!-- Missing hourly data intentionally -->
    </day>
</weather>'''
    
    with open('hourly_weather.xml', 'w', encoding='utf-8') as f:
        f.write(xml_content)
    
    print("Sample XML file created: hourly_weather.xml")

def parse_xml_buggy(filename):
    """
    Parse XML file with hourly weather data
    BUG: Contains several intentional bugs
    """
    try:
        tree = ET.parse(filename)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return None
    
    # BUG 1: Not handling namespaces properly
    # Should define namespace map for proper element lookup
    
    days_data = []
    
    # BUG 2: Direct element search without namespace handling
    for day_elem in root.findall('.//{http://weather.example.com/default}day'):  # Hardcoded namespace
        date = day_elem.get('date')
        hourly_data = []
        
        # BUG 3: Not handling missing date attribute
        if not date:
            continue  # Should provide default or skip with warning
        
        for hour_elem in day_elem.findall('hour'):
            time = hour_elem.get('time')
            
            # BUG 4: Direct element access without namespace
            temp_elem = hour_elem.find('{http://weather.example.com/schema}temp')  # Hardcoded namespace
            wind_elem = hour_elem.find('{http://weather.example.com/schema}wind')  # Hardcoded namespace
            # BUG 5: Not handling missing elements gracefully
            temp = float(temp_elem.text) if temp_elem is not None else None
            wind = float(wind_elem.text) if wind_elem is not None else None
            
            # BUG 6: Not validating time format
            hourly_data.append({
                'time': time,
                'temperature': temp,
                'wind_speed': wind
            })
        
        # BUG 7: Not handling days with no hourly data
        days_data.append({
            'date': date,
            'hourly': hourly_data
        })
    
    return days_data

def find_peak_hours_buggy(normalized_data):
    """
    Find peak temperature hour for each day
    BUG: Contains bugs in peak finding logic
    """
    peak_hours = []
    
    for day_data in normalized_data:
        date = day_data['date']
        hourly = day_data['hourly']
        
        if not hourly:
            # BUG 8: Poor handling of missing hourly data
            peak_hours.append({
                'date': date,
                'peak_hour': '12:00',  # Hardcoded default
                'peak_temp': 0.0       # Should use better default
            })
            continue
        
        # Find peak temperature
        max_temp = None
        peak_hour = None
        
        for hour_data in hourly:
            temp = hour_data.get('temperature')
            time = hour_data.get('time')
            
            # BUG 9: Not handling None temperatures
            if max_temp is None or temp > max_temp:
                max_temp = temp
                peak_hour = time
        
        peak_hours.append({
            'date': date,
            'peak_hour': peak_hour,
            'peak_temp': max_temp
        })
    
    return peak_hours

def save_results_buggy(normalized_data, peak_hours):
    """Save normalized data and peak hours"""
    
    # Save normalized JSON
    with open('normalized_hourly_buggy.json', 'w') as f:
        json.dump(normalized_data, f, indent=2)
    
    # Save peak hours CSV
    df = pd.DataFrame(peak_hours)
    df.to_csv('peak_hours_buggy.csv', index=False)
    
    print("Results saved to normalized_hourly_buggy.json and peak_hours_buggy.csv")

def main_xml_parsing_buggy():
    """Main function for XML parsing (buggy version)"""
    print("=== Task E: Parse Hourly Weather XML (BUGGY VERSION) ===")
    
    # Create sample XML
    create_sample_xml_data()
    
    # Parse XML
    print("Parsing XML file...")
    normalized_data = parse_xml_buggy('hourly_weather.xml')
    
    if not normalized_data:
        print("Failed to parse XML")
        return None
    
    print(f"Parsed {len(normalized_data)} days")
    
    # Find peak hours
    peak_hours = find_peak_hours_buggy(normalized_data)
    
    # Save results
    save_results_buggy(normalized_data, peak_hours)
    
    print("First normalized day object:")
    if normalized_data:
        print(json.dumps(normalized_data[0], indent=2))
    
    return normalized_data, peak_hours

# Run buggy version
if __name__ == "__main__":
    result_buggy = main_xml_parsing_buggy()


# Demo Cell - Show Expected Results
print("TASK E DEMONSTRATION")
print("=" * 50)

# Show sample normalized day object (what should be produced)
sample_normalized_day = {
    "date": "2024-08-18",
    "hourly": [
        {"time": "00:00", "temperature": 22.1, "wind_speed": 12.5},
        {"time": "03:00", "temperature": 21.8, "wind_speed": 13.2},
        {"time": "06:00", "temperature": 24.5, "wind_speed": 15.8},
        {"time": "09:00", "temperature": 28.3, "wind_speed": 18.1},
        {"time": "12:00", "temperature": 32.1, "wind_speed": 20.3},
        {"time": "15:00", "temperature": 34.2, "wind_speed": 22.7},
        {"time": "18:00", "temperature": 31.5, "wind_speed": 19.4},
        {"time": "21:00", "temperature": 26.8, "wind_speed": 16.2}
    ]
}

print("REQUESTED OUTPUT:")
print("First normalized day object:")
print(json.dumps(sample_normalized_day, indent=2))
