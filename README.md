# Task A - Table Scraping README

## Description
This project extracts HTML tables from Wikipedia pages and saves them as both CSV and JSON formats.

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
Run the notebook cell to execute the scraping script. The code includes error handling and fallback mechanisms.