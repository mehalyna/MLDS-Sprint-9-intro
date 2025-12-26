# Task B - Seven-day Forecast & Anomaly Detection Implementation
import requests
import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def fetch_weather_forecast(latitude=52.52, longitude=13.41, days=7):
    """
    Fetch 7-day weather forecast using Open-Meteo API
    Default location: Berlin, Germany
    """
    # Open-Meteo API endpoint
    url = "https://api.open-meteo.com/v1/forecast"
    
    # API parameters
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'daily': 'temperature_2m_max,temperature_2m_min',
        'timezone': 'auto',
        'forecast_days': days
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return None

def detect_temperature_anomalies(temperatures, dates):
    """
    Detect temperature anomalies using mean and standard deviation
    BUG: Contains several intentional bugs for educational purposes
    """
    # Convert to numpy array for calculations
    temps = np.array(temperatures)
    
    # BUG 1: Not checking for empty or invalid data
    # Should validate that temps is not empty and contains valid numbers
    
    # Calculate mean and standard deviation
    # BUG 2: Using population std instead of sample std without documenting choice
    mean_temp = np.mean(temps)
    std_temp = np.std(temps)  # This uses population std (ddof=0)
    
    # BUG 3: Hardcoded threshold without making it configurable
    threshold = 2 * std_temp
    
    # Find anomalies
    anomalies = []
    anomaly_indices = []
    
    for i, temp in enumerate(temps):
        deviation = abs(temp - mean_temp)
        if deviation > threshold:
            # BUG 4: Not handling potential index out of bounds
            anomalies.append(dates[i + 1])  # Off-by-one error potential
            anomaly_indices.append(i)
    
    return {
        'mean': mean_temp,
        'std': std_temp,
        'anomalies': anomalies,
        'anomaly_indices': anomaly_indices,
        'threshold': threshold
    }

def save_weekly_summary(analysis_results, filename='weekly_summary.json'):
    """
    Save the analysis results to JSON file
    """
    # Prepare summary data
    summary = {
        'mean': round(analysis_results['mean'], 2),
        'std': round(analysis_results['std'], 2),
        'anomalies': analysis_results['anomalies']
    }
    
    # BUG 5: Not handling potential file write errors
    with open(filename, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"Weekly summary saved to {filename}")
    return summary

def main_analysis():
    """
    Main function to run the 7-day forecast analysis
    """
    print("=== Task B: Seven-day Forecast & Anomaly Detection ===")
    
    # Fetch weather data
    print("Fetching 7-day weather forecast...")
    weather_data = fetch_weather_forecast()
    
    if not weather_data:
        print("Failed to fetch weather data!")
        return None
    
    # Extract temperature data
    daily_data = weather_data.get('daily', {})
    dates = daily_data.get('time', [])
    max_temperatures = daily_data.get('temperature_2m_max', [])
    
    print(f"Retrieved data for {len(dates)} days")
    print(f"Dates: {dates}")
    print(f"Max temperatures: {max_temperatures}")
    
    # BUG 6: Not properly validating array lengths as suggested in hints
    # Should check if len(dates) == len(max_temperatures)
    
    # Perform anomaly detection
    print("\nPerforming anomaly detection...")
    analysis = detect_temperature_anomalies(max_temperatures, dates)
    
    # Display results
    print(f"\nAnalysis Results:")
    print(f"Mean temperature: {analysis['mean']:.2f}°C")
    print(f"Standard deviation: {analysis['std']:.2f}°C")
    print(f"Anomaly threshold: {analysis['threshold']:.2f}°C")
    print(f"Detected anomalies: {analysis['anomalies']}")
    
    # Save to JSON
    summary = save_weekly_summary(analysis)
    
    return analysis

# Demo execution
if __name__ == "__main__":
    result = main_analysis()


# Demo Cell - Run Analysis and Show Mean, Std (Run-and-paste check)
print("=== TASK B DEMO OUTPUT ===")

# Run the analysis
analysis_result = main_analysis()

if analysis_result:
    print(f"\n REQUESTED VALUES FOR COPY-PASTE:")
    print(f"Mean: {analysis_result['mean']:.2f}")
    print(f"Std: {analysis_result['std']:.2f}")
    
    # Also show the full summary
    try:
        with open('weekly_summary.json', 'r') as f:
            summary = json.load(f)
        print(f"\n📄 Generated weekly_summary.json:")
        print(json.dumps(summary, indent=2))
    except FileNotFoundError:
        print("weekly_summary.json not found")
else:
    print(" Analysis failed!")

print("\n=== END DEMO OUTPUT ===")


# Task B - Seven-day Forecast & Anomaly Detection (BUG-FIXED VERSION)
import requests
import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def fetch_weather_forecast_fixed(latitude=52.52, longitude=13.41, days=7):
    """
    Fetch 7-day weather forecast using Open-Meteo API
    Default location: Berlin, Germany
    FIXES: Added better error handling and validation
    """
    # Validate inputs
    if not (-90 <= latitude <= 90):
        raise ValueError(f"Invalid latitude: {latitude}. Must be between -90 and 90.")
    if not (-180 <= longitude <= 180):
        raise ValueError(f"Invalid longitude: {longitude}. Must be between -180 and 180.")
    if not (1 <= days <= 16):
        raise ValueError(f"Invalid days: {days}. Must be between 1 and 16.")
    
    # Open-Meteo API endpoint
    url = "https://api.open-meteo.com/v1/forecast"
    
    # API parameters
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'daily': 'temperature_2m_max,temperature_2m_min',
        'timezone': 'auto',
        'forecast_days': days
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Validate response structure
        if 'daily' not in data:
            raise ValueError("Invalid API response: missing 'daily' data")
        
        return data
    except requests.exceptions.Timeout:
        raise ValueError("Request timed out. Please check your internet connection.")
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Failed to fetch weather data: {e}")
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON response from API")

def detect_temperature_anomalies_fixed(temperatures, dates, threshold_multiplier=2.0, use_sample_std=True):
    """
    Detect temperature anomalies using mean and standard deviation
    FIXES: All bugs from the original version have been addressed
    """
    # FIX 1: Validate input data
    if not temperatures:
        raise ValueError("Temperature list is empty")
    if not dates:
        raise ValueError("Dates list is empty")
    if len(temperatures) != len(dates):
        raise ValueError(f"Length mismatch: {len(temperatures)} temperatures vs {len(dates)} dates")
    
    # Convert to numpy array and validate numeric data
    try:
        temps = np.array(temperatures, dtype=float)
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid temperature data: {e}")
    
    # Check for NaN or infinite values
    if np.any(np.isnan(temps)) or np.any(np.isinf(temps)):
        raise ValueError("Temperature data contains NaN or infinite values")
    
    # Need at least 2 data points for meaningful statistics
    if len(temps) < 2:
        raise ValueError("Need at least 2 temperature measurements for anomaly detection")
    
    # FIX 2: Document choice of standard deviation and make it configurable
    # Using sample standard deviation (ddof=1) by default as it's more appropriate for small samples
    mean_temp = np.mean(temps)
    if use_sample_std:
        std_temp = np.std(temps, ddof=1)  # Sample standard deviation
        std_type = "sample"
    else:
        std_temp = np.std(temps, ddof=0)  # Population standard deviation
        std_type = "population"
    
    # FIX 3: Make threshold configurable
    threshold = threshold_multiplier * std_temp
    
    # Find anomalies with proper bounds checking
    anomalies = []
    anomaly_indices = []
    anomaly_details = []
    
    for i, temp in enumerate(temps):
        deviation = abs(temp - mean_temp)
        if deviation > threshold:
            # FIX 4: Proper bounds checking - no off-by-one error
            if i < len(dates):  # This should always be true given our validation above
                anomalies.append(dates[i])
                anomaly_indices.append(i)
                anomaly_details.append({
                    'date': dates[i],
                    'temperature': float(temp),
                    'deviation': float(deviation),
                    'threshold': float(threshold)
                })
    
    return {
        'mean': float(mean_temp),
        'std': float(std_temp),
        'std_type': std_type,
        'threshold_multiplier': threshold_multiplier,
        'threshold': float(threshold),
        'anomalies': anomalies,
        'anomaly_indices': anomaly_indices,
        'anomaly_details': anomaly_details,
        'total_data_points': len(temps)
    }

def save_weekly_summary_fixed(analysis_results, filename='weekly_summary_fixed.json'):
    """
    Save the analysis results to JSON file
    FIX 5: Added proper error handling for file operations
    """
    # Prepare summary data with more detail
    summary = {
        'mean': round(analysis_results['mean'], 2),
        'std': round(analysis_results['std'], 2),
        'std_type': analysis_results['std_type'],
        'threshold_multiplier': analysis_results['threshold_multiplier'],
        'threshold': round(analysis_results['threshold'], 2),
        'anomalies': analysis_results['anomalies'],
        'total_data_points': analysis_results['total_data_points'],
        'analysis_timestamp': datetime.now().isoformat()
    }
    
    try:
        # Ensure the file can be written
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        print(f" Weekly summary saved successfully to {filename}")
        return summary
    except IOError as e:
        raise IOError(f"Failed to write to {filename}: {e}")
    except Exception as e:
        raise Exception(f"Unexpected error saving summary: {e}")

def main_analysis_fixed(latitude=52.52, longitude=13.41, threshold_multiplier=2.0, use_sample_std=True):
    """
    Main function to run the 7-day forecast analysis (FIXED VERSION)
    FIX 6: Added comprehensive validation and error handling
    """
    print("=== Task B: Seven-day Forecast & Anomaly Detection (FIXED VERSION) ===")
    
    try:
        # Fetch weather data with validation
        print("Fetching 7-day weather forecast...")
        weather_data = fetch_weather_forecast_fixed(latitude, longitude, days=7)
        
        # Extract and validate temperature data
        daily_data = weather_data.get('daily', {})
        dates = daily_data.get('time', [])
        max_temperatures = daily_data.get('temperature_2m_max', [])
        
        print(f"Retrieved data for {len(dates)} days")
        print(f"Dates: {dates}")
        print(f"Max temperatures: {max_temperatures}")
        
        # FIX 6: Proper validation of array lengths (as suggested in hints)
        if len(dates) != len(max_temperatures):
            raise ValueError(f"Data mismatch: {len(dates)} dates vs {len(max_temperatures)} temperatures")
        
        if not dates or not max_temperatures:
            raise ValueError("No temperature data received from API")
        
        # Perform anomaly detection with fixed implementation
        print("\nPerforming anomaly detection...")
        analysis = detect_temperature_anomalies_fixed(
            max_temperatures, 
            dates, 
            threshold_multiplier=threshold_multiplier,
            use_sample_std=use_sample_std
        )
        
        # Display detailed results
        print(f"\n Analysis Results:")
        print(f"Mean temperature: {analysis['mean']:.2f}°C")
        print(f"Standard deviation: {analysis['std']:.2f}°C ({analysis['std_type']})")
        print(f"Anomaly threshold: ±{analysis['threshold']:.2f}°C ({threshold_multiplier}σ)")
        print(f"Data points analyzed: {analysis['total_data_points']}")
        
        if analysis['anomalies']:
            print(f" Detected {len(analysis['anomalies'])} anomalies: {analysis['anomalies']}")
            for detail in analysis['anomaly_details']:
                print(f"  - {detail['date']}: {detail['temperature']:.1f}°C (deviation: {detail['deviation']:.1f}°C)")
        else:
            print(" No anomalies detected (all temperatures within threshold)")
        
        # Save to JSON with error handling
        summary = save_weekly_summary_fixed(analysis)
        
        return analysis
        
    except Exception as e:
        print(f" Analysis failed: {e}")
        return None

# Demo execution of fixed version
def demo_fixed_analysis():
    """Run the fixed analysis and compare with original"""
    print(" Running FIXED implementation...")
    print("=" * 60)
    
    # Test with different parameters to show configurability
    result = main_analysis_fixed(
        latitude=52.52,  # Berlin
        longitude=13.41,
        threshold_multiplier=2.0,  # 2-sigma threshold
        use_sample_std=True  # Use sample standard deviation
    )
    
    if result:
        print(f"\n FIXED VERSION - REQUESTED VALUES FOR COPY-PASTE:")
        print(f"Mean: {result['mean']:.2f}")
        print(f"Std: {result['std']:.2f}")
        print(f"Standard deviation type: {result['std_type']}")
        
        # Show the improved JSON output
        try:
            with open('weekly_summary_fixed.json', 'r') as f:
                summary = json.load(f)
            print(f"\n📄 Generated weekly_summary_fixed.json:")
            print(json.dumps(summary, indent=2))
        except FileNotFoundError:
            print("weekly_summary_fixed.json not found")
    
    return result

if __name__ == "__main__":
    fixed_result = demo_fixed_analysis()


# Demo Cell - Run FIXED Analysis and Compare Results
print("🔧 RUNNING BUG-FIXED VERSION")
print("=" * 50)

# Run the fixed analysis
fixed_result = demo_fixed_analysis()

print("\n" + "=" * 50)
print(" COMPARISON: BUGGY vs FIXED VERSION")
print("=" * 50)

# Compare results if both analyses succeeded
if 'analysis_result' in globals() and fixed_result:
    print(" BUGGY VERSION:")
    print(f"   Mean: {analysis_result['mean']:.2f}°C")
    print(f"   Std: {analysis_result['std']:.2f}°C (type: unknown)")
    print(f"   Anomalies: {len(analysis_result['anomalies'])}")
    
    print("\n FIXED VERSION:")
    print(f"   Mean: {fixed_result['mean']:.2f}°C") 
    print(f"   Std: {fixed_result['std']:.2f}°C (type: {fixed_result['std_type']})")
    print(f"   Anomalies: {len(fixed_result['anomalies'])}")
    print(f"   Data points validated: {fixed_result['total_data_points']}")
    
    print(f"\n DIFFERENCES:")
    mean_diff = abs(analysis_result['mean'] - fixed_result['mean'])
    std_diff = abs(analysis_result['std'] - fixed_result['std'])
    print(f"   Mean difference: {mean_diff:.4f}°C")
    print(f"   Std difference: {std_diff:.4f}°C")
    
    if mean_diff < 0.01 and std_diff < 0.01:
        print("    Results are numerically identical (bugs didn't affect this dataset)")
    else:
        print("    Results differ (bugs affected the calculations)")

print(f"\n FINAL ANSWER (FIXED VERSION):")
print(f"Mean: {fixed_result['mean']:.2f}")
print(f"Std: {fixed_result['std']:.2f}")
