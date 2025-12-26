# Task D - Missing Data Detection & Simple Imputation (BUGGY VERSION)
import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def create_sample_data_with_gaps():
    """Create sample weather data with missing values"""
    data = {
        "city": "Tokyo",
        "weather_data": [
            {"date": "2024-08-15", "temp_max": 32.5, "temp_min": 22.1, "humidity": 65, "wind_speed": 15.2},
            {"date": "2024-08-16", "temp_max": None, "temp_min": 21.8, "humidity": 68, "wind_speed": None},
            {"date": "2024-08-17", "temp_max": 31.2, "temp_min": None, "humidity": None, "wind_speed": 18.5},
            {"date": "2024-08-18", "temp_max": None, "temp_min": None, "humidity": 72, "wind_speed": 16.8},
            {"date": "2024-08-19", "temp_max": 33.8, "temp_min": 23.5, "humidity": None, "wind_speed": None},
            {"date": "2024-08-20", "temp_max": 34.1, "temp_min": 24.2, "humidity": 58, "wind_speed": 14.3},
            {"date": "2024-08-21", "temp_max": None, "temp_min": 23.8, "humidity": 61, "wind_speed": 17.2},
            {"date": "2024-08-22", "temp_max": 30.9, "temp_min": None, "humidity": None, "wind_speed": None}
        ]
    }
    
    with open('tokyo_weather_gaps.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print(" Sample data with gaps created: tokyo_weather_gaps.json")
    return data

def linear_interpolation_buggy(values):
    """
    Linear interpolation for missing values
    BUG: Contains several intentional bugs
    """
    if not values:
        return values
    
    # Convert to numpy array
    arr = np.array(values, dtype=float)
    
    # BUG 1: Not handling edge cases (leading/trailing nulls)
    # Should propagate nearest non-null values for edge cases
    
    # Find missing values
    missing_mask = np.isnan(arr)
    
    if not np.any(missing_mask):
        return values  # No missing values
    
    # BUG 2: Not checking if >50% values are missing
    # Should flag for manual review if too many missing
    
    # Simple linear interpolation
    valid_indices = np.where(~missing_mask)[0]
    
    if len(valid_indices) < 2:
        # BUG 3: Poor handling when insufficient data points
        return values  # Should handle this case better
    
    for i in range(len(arr)):
        if missing_mask[i]:
            # Find nearest valid values
            left_idx = None
            right_idx = None
            
            # Find left boundary
            for j in range(i-1, -1, -1):
                if not missing_mask[j]:
                    left_idx = j
                    break
            
            # Find right boundary  
            for j in range(i+1, len(arr)):
                if not missing_mask[j]:
                    right_idx = j
                    break
            
            # BUG 4: Incorrect interpolation when boundaries missing
            if left_idx is not None and right_idx is not None:
                # Linear interpolation
                x1, y1 = left_idx, arr[left_idx]
                x2, y2 = right_idx, arr[right_idx]
                arr[i] = y1 + (y2 - y1) * (i - x1) / (x2 - x1)
            elif left_idx is not None:
                arr[i] = arr[left_idx]  # Forward fill
            elif right_idx is not None:
                arr[i] = arr[right_idx]  # Backward fill
    
    return arr.tolist()

def moving_average_imputation_buggy(values, window=3):
    """
    Moving average imputation for wind/humidity
    BUG: Contains bugs in implementation
    """
    if not values:
        return values
    
    arr = np.array(values, dtype=float)
    missing_mask = np.isnan(arr)
    
    if not np.any(missing_mask):
        return values
    
    # BUG 5: Window size not adjusted for data length
    # Should adjust window size if data is too short
    
    for i in range(len(arr)):
        if missing_mask[i]:
            # Calculate moving average
            start = max(0, i - window//2)
            end = min(len(arr), i + window//2 + 1)
            
            window_values = arr[start:end]
            valid_values = window_values[~np.isnan(window_values)]
            
            if len(valid_values) > 0:
                arr[i] = np.mean(valid_values)
            # BUG 6: No fallback when no valid values in window
    
    return arr.tolist()

def impute_weather_data_buggy(data):
    """
    Impute missing values in weather data
    BUG: Poor tracking of imputation counts
    """
    imputed_data = json.loads(json.dumps(data))  # Deep copy
    imputation_counts = {}
    
    weather_records = imputed_data.get('weather_data', [])
    
    # Extract field arrays
    fields = ['temp_max', 'temp_min', 'humidity', 'wind_speed']
    field_arrays = {}
    
    for field in fields:
        field_arrays[field] = [record.get(field) for record in weather_records]
    
    # Impute each field
    for field, values in field_arrays.items():
        original_values = values.copy()
        
        if field in ['temp_max', 'temp_min']:
            # Use linear interpolation for temperatures
            imputed_values = linear_interpolation_buggy(values)
        else:
            # Use moving average for humidity and wind
            imputed_values = moving_average_imputation_buggy(values)
        
        # BUG 7: Incorrect counting of imputed values
        # Should count actual None -> value changes
        count = sum(1 for i, v in enumerate(original_values) if v is None)
        imputation_counts[field] = count
        
        # Update records
        for i, record in enumerate(weather_records):
            if i < len(imputed_values):
                record[field] = imputed_values[i]
    
    return imputed_data, imputation_counts

def main_imputation_buggy():
    """Main function for buggy imputation process"""
    print("=== Task D: Missing Data Imputation (BUGGY VERSION) ===")
    
    # Create sample data
    original_data = create_sample_data_with_gaps()
    
    # Perform imputation
    print("\n Performing imputation...")
    imputed_data, counts = impute_weather_data_buggy(original_data)
    
    # Save results
    with open('tokyo_imputed_buggy.json', 'w') as f:
        json.dump(imputed_data, f, indent=2)
    
    report = {"imputed_counts": counts}
    with open('imputation_report_buggy.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print(" Imputation complete (buggy version)")
    print(f" Imputation counts: {counts}")
    
    return report

# Run buggy version
if __name__ == "__main__":
    result_buggy = main_imputation_buggy()


# Demo Cell - Run Both Versions and Show Results
print(" RUNNING BOTH VERSIONS")
print("=" * 50)

# Run buggy version
print(" BUGGY VERSION:")
result_buggy = main_imputation_buggy()

print("\n" + "=" * 50)

print(f"\n REQUESTED OUTPUT (Buggy Version):")
print(f"imputation_report['imputed_counts'] = {result_buggy['imputed_counts']}")
