# Task F - Free-text Weather Extraction (BUGGY VERSION)
import re
import pandas as pd
from datetime import datetime

def create_sample_weather_logs():
    """Create sample free-text weather logs with various formats"""
    weather_logs = """2024-08-18: Máximo 87°F, mínimo 72°F, humedad 65%, precipitación 0,0mm
August 19, 2024 - High: 91F Low: 75F Humidity: 72% Rain: 2.5mm
20/08/2024 Max temp: 32,9°C Min: 22,5°C Humid: 58% Precip: 0.0
2024-08-21 Maximum temperature 89°F minimum 74°F humidity 68% precipitation 1,2 millimeters
Aug 22 '24: TOP 35.1°C BOTTOM 25.7°C H=63% P=0mm
23.08.2024 - Høy: 88°F Lav: 71°F Fuktighet: 59% Nedbør: 0,5mm
24-Aug-2024: Max 33.8C Min 24.1C Humidity 61% Rain 0.0mm
2024/08/25 High temp 90°F Low temp 73°F RH 66% Precipitation 3,1mm"""
    
    with open('weather_logs.txt', 'w', encoding='utf-8') as f:
        f.write(weather_logs)
    
    print("Sample weather logs created: weather_logs.txt")

def normalize_number_buggy(text):
    """
    Normalize number with decimal separator
    BUG: Not handling all cases properly
    """
    if not text:
        return None
    
    # BUG 1: Not handling spaces in numbers
    text = text.strip()
    
    # BUG 2: Simple comma to dot replacement without validation
    text = text.replace(',', '.')
    
    try:
        return float(text)
    except ValueError:
        return None

def fahrenheit_to_celsius_buggy(temp):
    """
    Convert Fahrenheit to Celsius
    BUG: Contains calculation error
    """
    if temp is None:
        return None
    
    # BUG 3: Wrong conversion formula
    return (temp - 32) * 5 / 8  # Should be 5/9

def detect_fahrenheit_buggy(temp_text, temp_value):
    """
    Detect if temperature is in Fahrenheit
    BUG: Poor detection logic
    """
    if not temp_text or temp_value is None:
        return False
    
    # BUG 4: Only checking for 'F' but not '°F'
    if 'F' in temp_text.upper():
        return True
    
    # BUG 5: Wrong threshold for Fahrenheit detection
    if temp_value > 50:  # Should be around 60
        return True
    
    return False

def extract_weather_data_buggy(text):
    """
    Extract weather data from free text
    BUG: Contains multiple regex and parsing bugs
    """
    # BUG 6: Limited date patterns
    date_patterns = [
        r'(\d{4}-\d{2}-\d{2})',
        r'(\d{2}/\d{2}/\d{4})',
        r'(\w+ \d{1,2}, \d{4})'
    ]
    
    # BUG 7: Incomplete temperature patterns
    temp_patterns = [
        r'(?:max|máximo|high|høy|top).*?(\d+(?:[,.]\d+)?)\s*°?([CF])?',
        r'(?:min|mínimo|low|lav|bottom).*?(\d+(?:[,.]\d+)?)\s*°?([CF])?'
    ]
    
    # BUG 8: Basic humidity pattern missing variations
    humidity_pattern = r'(?:humidity|humedad|humid|fuktighet|h).*?(\d+(?:[,.]\d+)?)'
    
    # BUG 9: Incomplete precipitation patterns
    precip_patterns = [
        r'(?:rain|precipitation|precipitación|precip|nedbør|p).*?(\d+(?:[,.]\d+)?)',
    ]
    
    extracted = {}
    
    # Extract date
    date_found = False
    for pattern in date_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            extracted['date'] = match.group(1)
            date_found = True
            break
    
    # BUG 10: No fallback for missing date
    if not date_found:
        extracted['date'] = None
    
    # Extract temperatures
    max_temp = None
    min_temp = None
    
    # BUG 11: Only checking first pattern
    for pattern in temp_patterns[:1]:  # Should check all patterns
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            for match in matches:
                temp_str, unit = match
                temp_val = normalize_number_buggy(temp_str)
                
                if detect_fahrenheit_buggy(temp_str + unit, temp_val):
                    temp_val = fahrenheit_to_celsius_buggy(temp_val)
                
                # BUG 12: Poor max/min assignment logic
                if max_temp is None:
                    max_temp = temp_val
                else:
                    min_temp = temp_val
    
    extracted['max_temp'] = max_temp
    extracted['min_temp'] = min_temp
    
    # Extract humidity
    humidity_match = re.search(humidity_pattern, text, re.IGNORECASE)
    if humidity_match:
        extracted['humidity'] = normalize_number_buggy(humidity_match.group(1))
    else:
        extracted['humidity'] = None
    
    # Extract precipitation
    precipitation = None
    for pattern in precip_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            precipitation = normalize_number_buggy(match.group(1))
            break
    
    extracted['precipitation'] = precipitation
    
    return extracted

def save_patterns_buggy():
    """Save regex patterns to file"""
    patterns = """Date Patterns:
(\\d{4}-\\d{2}-\\d{2})
(\\d{2}/\\d{2}/\\d{4})
(\\w+ \\d{1,2}, \\d{4})

Temperature Patterns:
(?:max|máximo|high|høy|top).*?(\\d+(?:[,.]\\d+)?)\\s*°?([CF])?

Humidity Pattern:
(?:humidity|humedad|humid|fuktighet|h).*?(\\d+(?:[,.]\\d+)?)

Precipitation Pattern:
(?:rain|precipitation|precipitación|precip|nedbør|p).*?(\\d+(?:[,.]\\d+)?)"""
    
    with open('patterns_buggy.txt', 'w', encoding='utf-8') as f:
        f.write(patterns)

def main_weather_extraction_buggy():
    """Main function for weather extraction (buggy version)"""
    print("=== Task F: Free-text Weather Extraction (BUGGY VERSION) ===")
    
    # Create sample data
    create_sample_weather_logs()
    
    # Read and process logs
    with open('weather_logs.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    extracted_data = []
    
    print("Processing weather logs...")
    for i, line in enumerate(lines):
        line = line.strip()
        if line:
            print(f"Line {i+1}: {line}")
            result = extract_weather_data_buggy(line)
            print(f"Extracted: {result}")
            extracted_data.append(result)
            print()
    
    # Save to CSV
    df = pd.DataFrame(extracted_data)
    df.columns = ['Date', 'Max Temperature', 'Min Temperature', 'Humidity', 'Precipitation']
    df.to_csv('extracted_weather_data_buggy.csv', index=False)
    
    # Save patterns
    save_patterns_buggy()
    
    print("Results saved to extracted_weather_data_buggy.csv and patterns_buggy.txt")
    
    # Show first extraction for paste-and-check
    if extracted_data:
        print("First extraction result:")
        print(extracted_data[0])
    
    return extracted_data

# Run buggy version
if __name__ == "__main__":
    result_buggy = main_weather_extraction_buggy()
