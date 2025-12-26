# MLDS Sprint 9: Data Acquisition and Preprocessing

This repository contains practical implementations for data acquisition and preprocessing tasks, focusing on web scraping, API integration, data normalization, missing data imputation, XML parsing, and text extraction.

## Overview

This project demonstrates various data engineering techniques commonly used in machine learning and data science pipelines. Each task includes both a buggy implementation (for educational purposes) and a corrected version with comprehensive fixes and best practices.

---

## Task A: Table Scraping Implementation

**Objective**: Scrape structured data from Wikipedia tables and convert it to standardized formats (CSV and JSON).

### Description
Implement a web scraper that:
- Fetches HTML content from Wikipedia pages
- Parses HTML tables using BeautifulSoup
- Handles different table structures and edge cases
- Cleans and normalizes scraped data
- Exports results to both CSV and JSON formats

### Key Concepts
- Web scraping with `requests` and `BeautifulSoup`
- HTML table parsing and data extraction
- Text cleaning and normalization (removing footnotes, whitespace)
- Data validation and error handling
- Multi-format data export (CSV/JSON)

### Intentional Bugs (Educational)
1. Off-by-one error in table indexing
2. Missing validation for column count consistency
3. Blanket `fillna()` without selective handling

### Deliverables
- `table_data.csv` - Scraped data in CSV format
- `table_data.json` - Scraped data in JSON format
- First 3 records from scraped table

**File**: `example1.py`

---

## Task B: Seven-Day Forecast & Anomaly Detection

**Objective**: Fetch weather forecast data from an API and detect temperature anomalies using statistical methods.

### Description
Implement a weather analysis system that:
- Fetches 7-day weather forecasts from Open-Meteo API
- Calculates statistical measures (mean, standard deviation)
- Detects temperature anomalies using threshold-based method
- Generates analysis reports in JSON format

### Key Concepts
- RESTful API integration
- Statistical anomaly detection (z-score method)
- Standard deviation calculation (population vs sample)
- Array validation and bounds checking
- JSON data serialization

### Statistical Method
- **Mean temperature**: Average of all temperature readings
- **Standard deviation**: Measure of temperature variability
- **Anomaly threshold**: Temperatures beyond ±2σ (configurable)
- **Detection**: Flag days where temperature deviates significantly from mean

### Intentional Bugs (Educational)
1. No validation for empty or invalid data
2. Using population std instead of sample std (undocumented)
3. Hardcoded threshold (not configurable)
4. Off-by-one error in anomaly indexing
5. Missing file write error handling
6. No array length validation

### Deliverables
- `weekly_summary.json` - Analysis results with mean, std, and anomalies
- Mean and standard deviation values for 7-day forecast

**File**: `example2.py`

---

## Task C: Normalize & Combine Weather Files

**Objective**: Normalize weather data from multiple cities with different JSON schemas and combine into a unified format.

### Description
Implement a data normalization pipeline that:
- Reads JSON files from multiple sources (Tokyo, New York, London)
- Handles different schema structures and field names
- Normalizes date formats (ISO 8601, DD/MM/YYYY, timestamps)
- Combines normalized data into single CSV file
- Handles missing fields gracefully

### Data Schemas

**Schema 1 - Tokyo (Open-Meteo style)**:
```json
{
  "city": "Tokyo",
  "daily": {
    "time": ["2024-08-18", ...],
    "temperature_2m_max": [32.5, ...],
    ...
  }
}
```

**Schema 2 - New York (Weather API style)**:
```json
{
  "location": "New York",
  "forecast": [
    {
      "date": "18/08/2024",
      "temp_max": 28.3,
      ...
    }
  ]
}
```

**Schema 3 - London (Custom format)**:
```json
{
  "city_name": "London",
  "weather_data": [
    {
      "timestamp": "2024-08-18T00:00:00Z",
      "max_temperature": 24.1,
      ...
    }
  ]
}
```

### Key Concepts
- Schema mapping and data normalization
- Date format standardization
- Handling missing data fields
- Data validation and consistency checks
- Multi-source data integration

### Intentional Bugs (Educational)
1. Incorrect date format parsing (MM/DD vs DD/MM)
2. Missing date validation
3. No array length validation
4. KeyError when fields are missing
5. No data sorting by date
6. Poor error recovery for missing fields

### Deliverables
- `cities_comparison.csv` - Combined normalized weather data
- First CSV row with all fields

**File**: `example3.py`

---

## Task D: Missing Data Detection & Simple Imputation

**Objective**: Detect missing values in weather datasets and implement imputation strategies.

### Description
Implement data imputation algorithms that:
- Identify missing values (None/NaN) in time-series data
- Apply linear interpolation for temperature data
- Use moving average for humidity and wind speed
- Track imputation counts and methods used
- Generate comprehensive imputation reports

### Imputation Strategies

**Linear Interpolation** (for temperatures):
- Finds nearest valid values (left and right boundaries)
- Calculates intermediate values using linear formula
- Handles edge cases (leading/trailing nulls)

**Moving Average** (for humidity/wind):
- Uses sliding window of neighboring values
- Calculates mean of valid values in window
- Adjusts window size based on data availability

### Key Concepts
- Time-series data imputation
- Linear interpolation mathematics
- Moving average calculations
- Edge case handling (leading/trailing nulls)
- Data quality validation (>50% missing check)

### Intentional Bugs (Educational)
1. Not handling edge cases (leading/trailing nulls)
2. Missing validation for >50% missing data threshold
3. Poor handling with insufficient data points
4. Incorrect interpolation logic
5. Window size not adjusted for data length
6. No fallback when moving average fails
7. Incorrect counting of imputed values

### Deliverables
- `tokyo_imputed.json` - Dataset with imputed values
- `imputation_report.json` - Report with imputation counts per field

**File**: `example4.py`

---

## Task E: Parse Hourly Weather from XML

**Objective**: Parse XML files with namespaces to extract and normalize hourly weather data.

### Description
Implement an XML parser that:
- Parses XML files with namespace declarations
- Handles multiple namespace prefixes
- Extracts hourly weather data (temperature, wind speed)
- Validates time formats and data ranges
- Finds peak temperature hours for each day
- Exports to JSON and CSV formats

### XML Structure
```xml
<?xml version="1.0" encoding="UTF-8"?>
<weather xmlns:w="http://weather.example.com/schema" 
         xmlns="http://weather.example.com/default">
    <day date="2024-08-18">
        <hour time="00:00">
            <w:temp>22.1</w:temp>
            <w:wind>12.5</w:wind>
        </hour>
        <!-- More hours... -->
    </day>
</weather>
```

### Key Concepts
- XML parsing with ElementTree
- Namespace handling in XML (default and prefixed)
- XPath expressions with namespaces
- Data validation (date, time, temperature ranges)
- Peak value detection in time-series data

### Intentional Bugs (Educational)
1. Improper namespace handling (hardcoded URIs)
2. Missing date attribute validation
3. Direct element access without namespace awareness
4. No time format validation
5. Inadequate handling of missing XML elements
6. Poor validation of time format (HH:MM)
7. Hardcoded defaults for missing data
8. No None temperature handling in peak finding

### Deliverables
- `normalized_hourly.json` - Structured hourly weather data
- `peak_hours.csv` - Peak temperature hour for each day
- First normalized day object (JSON structure)

**File**: `example5.py`

---

## Task F: Free-Text Weather Extraction

**Objective**: Extract structured weather data from free-text logs using regular expressions.

### Description
Implement a text extraction system that:
- Parses weather data from unstructured text logs
- Handles multiple date formats and languages
- Extracts temperatures in Fahrenheit and Celsius
- Converts temperature units automatically
- Handles decimal separators (comma vs period)
- Extracts humidity and precipitation data
- Documents regex patterns used

### Sample Input Formats
```
2024-08-18: Máximo 87°F, mínimo 72°F, humedad 65%, precipitación 0,0mm
August 19, 2024 - High: 91F Low: 75F Humidity: 72% Rain: 2.5mm
20/08/2024 Max temp: 32,9°C Min: 22,5°C Humid: 58% Precip: 0.0
Aug 22 '24: TOP 35.1°C BOTTOM 25.7°C H=63% P=0mm
```

### Key Concepts
- Regular expressions (regex) for text extraction
- Multi-language pattern matching (English, Spanish, Norwegian)
- Temperature unit conversion (Fahrenheit ↔ Celsius)
- Number normalization (decimal separators)
- Date format parsing and standardization
- Pattern documentation and maintenance

### Regex Patterns
- **Dates**: ISO (YYYY-MM-DD), European (DD/MM/YYYY), US (Month DD, YYYY)
- **Temperatures**: Multiple keywords (max/máximo/high/høy/top, min/mínimo/low/lav)
- **Humidity**: Keywords in multiple languages (humidity/humedad/fuktighet)
- **Precipitation**: Various terms (rain/precipitation/precipitación/nedbør)

### Intentional Bugs (Educational)
1. Not handling spaces in numbers
2. Simple comma-to-dot replacement without context
3. Wrong Fahrenheit to Celsius formula (5/8 instead of 5/9)
4. Only checking for 'F' but not '°F'
5. Wrong Fahrenheit detection threshold (50 instead of 60)
6. Limited date pattern coverage
7. Incomplete temperature extraction patterns
8. Basic humidity pattern missing variations
9. Incomplete precipitation patterns
10. No fallback for missing dates
11. Only checking first temperature pattern
12. Poor max/min assignment logic

### Deliverables
- `extracted_weather_data.csv` - Structured extracted data
- `patterns.txt` - Documentation of regex patterns used
- First extraction result (all fields)

**File**: `example6.py`

---

## Project Structure

```
MLDS_sprint_9_intro/
├── README.md                          # This file
├── app.py                             # 🚀 Streamlit Visualization Dashboard
├── requirements.txt                   # Python dependencies
│
├── examples_py/                       # Python implementations
│   ├── example1.py                    # Task A: Table Scraping
│   ├── example2.py                    # Task B: Weather Forecast & Anomaly Detection
│   ├── example3.py                    # Task C: Normalize & Combine Weather Files
│   ├── example4.py                    # Task D: Missing Data Imputation
│   ├── example5.py                    # Task E: XML Parsing
│   └── example6.py                    # Task F: Free-text Extraction
│
├── examples_ipynb/                    # Jupyter Notebook versions
│   ├── example1.ipynb                 # Notebook version of Task A
│   ├── example2.ipynb                 # Notebook version of Task B
│   ├── example3.ipynb                 # Notebook version of Task C
│   ├── example4.ipynb                 # Notebook version of Task D
│   ├── example5.ipynb                 # Notebook version of Task E
│   └── example6.ipynb                 # Notebook version of Task F
│
└── [output files]                     # Generated data files
```

---

## Dependencies

Install all required dependencies using:

```bash
pip install -r requirements.txt
```

### Required Python Packages
- **requests**: HTTP library for API calls and web scraping
- **beautifulsoup4**: HTML/XML parsing library
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing for statistics
- **streamlit**: Interactive web dashboard framework
- **plotly**: Interactive visualization library
- **lxml**: Fast XML/HTML parsing (optional but recommended)

### Built-in Modules (No installation needed)
- **json**: JSON serialization
- **re**: Regular expressions
- **xml.etree.ElementTree**: XML parsing
- **datetime**: Date/time handling

---

## Running the Tasks

### Option 1: Interactive Streamlit Dashboard (Recommended) 🚀

Launch the interactive visualization dashboard to explore all results:

```bash
# Install dependencies first
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501` and provides:
- 📊 Interactive visualizations for all tasks
- 🔄 Toggle between buggy and fixed versions
- 📈 Charts, graphs, and statistical summaries
- 📥 Data export capabilities
- 🎯 Easy navigation between tasks

### Option 2: Run Individual Tasks

```bash
# Task A - Table Scraping
python examples_py/example1.py

# Task B - Weather Forecast & Anomaly Detection
python examples_py/example2.py

# Task C - Normalize & Combine Weather Files
python examples_py/example3.py

# Task D - Missing Data Imputation
python examples_py/example4.py

# Task E - XML Parsing
python examples_py/example5.py

# Task F - Free-text Extraction
python examples_py/example6.py
```

### Option 3: Using Jupyter Notebooks

```bash
jupyter notebook examples_ipynb/example1.ipynb
# ... and so on for other notebooks
```

---

## Educational Approach

Each task includes:

1. **Buggy Version**: Contains intentional bugs for learning purposes
   - Demonstrates common mistakes and pitfalls
   - Shows consequences of poor validation
   - Highlights importance of edge case handling

2. **Fixed Version**: Corrected implementation with best practices
   - Comprehensive input validation
   - Proper error handling
   - Edge case management
   - Clear documentation
   - Configurable parameters

3. **Demo Code**: Shows expected outputs and usage examples
   - Validates implementations
   - Provides copy-paste verification
   - Shows proper result formatting

---

## Learning Objectives

After completing these tasks, you should be able to:

1. **Web Scraping**: Extract structured data from HTML tables
2. **API Integration**: Fetch and process data from REST APIs
3. **Data Normalization**: Handle multiple data schemas and formats
4. **Missing Data**: Implement imputation strategies for time-series data
5. **XML Processing**: Parse XML with namespaces and complex structures
6. **Text Extraction**: Use regex to extract structured data from unstructured text
7. **Error Handling**: Implement comprehensive validation and error recovery
8. **Data Quality**: Validate data consistency and completeness
9. **Best Practices**: Write maintainable, documented, and robust code

---

## Common Patterns & Best Practices

### Data Validation
- Check for empty inputs before processing
- Validate array lengths match
- Verify data types and ranges
- Handle None/NaN values explicitly

### Error Handling
```python
try:
    # Operation
except SpecificException as e:
    # Handle specific error
    raise ValueError(f"Descriptive message: {e}")
```

### Configuration
- Make thresholds configurable (not hardcoded)
- Use parameters with sensible defaults
- Document parameter choices and reasoning

### Testing
- Validate with sample data first
- Check edge cases (empty, single value, all nulls)
- Verify output format and structure
- Compare buggy vs fixed implementations

---

## Output Files Generated

Each task generates specific output files:

**Task A**:
- `table_data.csv`, `table_data.json`

**Task B**:
- `weekly_summary.json`

**Task C**:
- `tokyo_weather.json`, `newyork_weather.json`, `london_weather.json`
- `cities_comparison.csv`

**Task D**:
- `tokyo_weather_gaps.json`
- `tokyo_imputed.json`
- `imputation_report.json`

**Task E**:
- `hourly_weather.xml`
- `normalized_hourly.json`
- `peak_hours.csv`

**Task F**:
- `weather_logs.txt`
- `extracted_weather_data.csv`
- `patterns.txt`

---

## Notes

- All tasks use realistic weather data examples
- Temperature units are standardized to Celsius in outputs
- Date formats are normalized to ISO 8601 (YYYY-MM-DD) where possible
- Code includes extensive comments explaining logic and decisions
- Both buggy and fixed versions are provided for comparison

---

## Author

MLDS Sprint 9 - Introduction to Data Acquisition and Preprocessing

---

## License

Educational use only. Sample code for learning purposes
- `table_data.csv`: CSV format with headers
- `table_data.json`: JSON array of objects format

## Usage
Run the notebook cells to execute the exercises. Each task includes both buggy and fixed versions for educational comparison.
