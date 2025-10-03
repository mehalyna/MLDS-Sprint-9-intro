# MLDS Sprint 9 - Data Science Exercises

This project contains data science exercises covering web scraping, API integration, data processing, and text analysis.

## Tasks Included

### Task A - Table Scraping
Extract HTML tables from Wikipedia pages and save them as CSV and JSON formats.

### Task B - Weather Forecast Analysis
Fetch weather data from APIs and perform anomaly detection.

### Task C - Data Normalization
Normalize multi-city weather data with different schemas.

### Task D - Data Imputation
Fill missing data using linear interpolation and moving averages.

### Task E - XML Parsing
Parse hourly weather XML data with namespace handling.

### Task F - Free-text Weather Extraction
Extract weather data from free-text logs using regex patterns.

## URLs Used

### Primary URL (Failed)
- **URL**: https://en.wikipedia.org/wiki/List_of_programming_languages
- **Table Index**: 0 (first table)
- **Status**: Failed due to bug in table selection logic

### Backup URL (Successful)
- **URL**: https://en.wikipedia.org/wiki/Comparison_of_programming_languages  
- **Table Index**: 0 (first table)
- **Status**: Successfully scraped and processed

## Table Information
- **Source**: Wikipedia comparison table of programming languages
- **Columns**: Language, Statements ratio, Lines ratio
- **Rows**: Multiple programming languages with their performance metrics
- **Format**: Clean text with footnote markers removed

## Known Bugs (Intentional)
This implementation contains several intentional bugs for educational purposes:

1. **Off-by-one Error**: `table_index + 1` causes IndexError when accessing tables array
2. **Column Count Mismatch**: No validation that row length matches header length
3. **Overly Aggressive Fill**: `fillna('')` applied to all columns without discrimination

## Output Files
- `table_data.csv`: CSV format with headers
- `table_data.json`: JSON array of objects format

## Usage
Run the notebook cells to execute the exercises. Each task includes both buggy and fixed versions for educational comparison.
