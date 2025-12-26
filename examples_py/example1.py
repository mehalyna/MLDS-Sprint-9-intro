# Task A - Table Scraping Implementation
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import re

def scrape_wikipedia_table(url, table_index=0):
    """
    Scrape a table from Wikipedia and return as DataFrame
    """
    # Get the webpage
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    # Parse HTML
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all tables
    tables = soup.find_all('table', class_='wikitable')
    
    if not tables:
        raise ValueError("No wikitable found on the page")
    
    # BUG 1: Off-by-one error - should check if table_index is within bounds
    table = tables[table_index + 1]  # This will cause IndexError for single table pages
    
    # Extract headers
    headers = []
    header_row = table.find('tr')
    if header_row:
        for th in header_row.find_all(['th', 'td']):
            # Clean header text
            header_text = th.get_text().strip()
            # Remove footnote markers
            header_text = re.sub(r'\[.*?\]', '', header_text)
            headers.append(header_text)
    
    # Extract rows
    rows = []
    for tr in table.find_all('tr')[1:]:  # Skip header row
        row = []
        for td in tr.find_all(['td', 'th']):
            # Clean cell text
            cell_text = td.get_text().strip()
            # Remove footnote markers and extra whitespace
            cell_text = re.sub(r'\[.*?\]', '', cell_text)
            cell_text = ' '.join(cell_text.split())
            row.append(cell_text)
        
        # BUG 2: Not handling rows with different column counts
        if row:  # Should check if len(row) == len(headers)
            rows.append(row)
    
    # Create DataFrame
    df = pd.DataFrame(rows, columns=headers)
    return df

def clean_and_normalize_data(df):
    """
    Clean and normalize the scraped data
    """
    # Remove empty rows
    df = df.dropna(how='all')
    
    # BUG 3: Not handling columns that might be completely empty
    # This could cause issues if some columns are all NaN
    df = df.fillna('')  # Should be more selective about which columns to fill
    
    return df

def save_data(df, csv_filename='table_data.csv', json_filename='table_data.json'):
    """
    Save DataFrame to CSV and JSON formats
    """
    # Save as CSV
    df.to_csv(csv_filename, index=False)
    
    # Save as JSON
    # Convert DataFrame to list of dictionaries
    data_dict = df.to_dict('records')
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(data_dict, f, indent=2, ensure_ascii=False)
    
    print(f"Data saved to {csv_filename} and {json_filename}")
    return df

# Demo execution
if __name__ == "__main__":
    # Wikipedia page with programming languages table
    url = "https://en.wikipedia.org/wiki/List_of_programming_languages"
    
    try:
        # Scrape the table
        print("Scraping Wikipedia table...")
        df = scrape_wikipedia_table(url, table_index=0)
        
        print(f"Table scraped successfully. Shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        
        # Clean and normalize
        df_clean = clean_and_normalize_data(df)
        
        # Save data
        final_df = save_data(df_clean)
        
        print("\nFirst 3 records:")
        print(final_df.head(3).to_string(index=False))
        
    except Exception as e:
        print(f"Error: {e}")
        print("Attempting to use backup table...")
        
        # Fallback to a simpler table if the main one fails
        backup_url = "https://en.wikipedia.org/wiki/Comparison_of_programming_languages"
        try:
            df = scrape_wikipedia_table(backup_url, table_index=0)
            df_clean = clean_and_normalize_data(df)
            final_df = save_data(df_clean)
            print("\nFirst 3 records from backup table:")
            print(final_df.head(3).to_string(index=False))
        except Exception as backup_error:
            print(f"Backup also failed: {backup_error}")


# Demo Cell - Show First 3 Records (Run-and-paste check)
print("=== TASK A DEMO OUTPUT ===")
print("First 3 records from scraped table:")
print()

# Read the CSV file to show the results
import pandas as pd
df_demo = pd.read_csv('table_data.csv')
print(df_demo.head(3).to_string(index=False))

print(f"\nTotal records: {len(df_demo)}")
print(f"Columns: {list(df_demo.columns)}")
print("\n=== END DEMO OUTPUT ===")


# Task A - Table Scraping Implementation (BUG-FIXED VERSION)
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import re

def scrape_wikipedia_table_fixed(url, table_index=0):
    """
    Scrape a table from Wikipedia and return as DataFrame
    FIXES APPLIED:
    - Fixed off-by-one error in table selection
    - Added validation for column count consistency
    - Better error handling for edge cases
    """
    # Get the webpage
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        raise ValueError(f"Failed to fetch webpage: {e}")
    
    # Parse HTML
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all tables (try multiple selectors)
    tables = soup.find_all('table', class_='wikitable')
    if not tables:
        tables = soup.find_all('table', class_='sortable')
    if not tables:
        tables = soup.find_all('table')
    
    if not tables:
        raise ValueError("No tables found on the page")
    
    # FIX 1: Proper bounds checking instead of off-by-one error
    if table_index >= len(tables):
        raise ValueError(f"Table index {table_index} out of range. Found {len(tables)} tables.")
    
    table = tables[table_index]  # FIXED: removed the +1
    
    # Extract headers with better logic
    headers = []
    header_row = table.find('tr')
    
    if header_row:
        # Try to find proper header cells (th elements first, then td if needed)
        header_cells = header_row.find_all('th')
        if not header_cells:
            header_cells = header_row.find_all('td')
            
        for cell in header_cells:
            # Clean header text
            header_text = cell.get_text().strip()
            # Remove footnote markers, citations, and extra whitespace
            header_text = re.sub(r'\[.*?\]', '', header_text)
            header_text = re.sub(r'\s+', ' ', header_text)
            header_text = header_text.strip()
            
            # Handle empty headers
            if not header_text:
                header_text = f"Column_{len(headers)}"
                
            headers.append(header_text)
    
    if not headers:
        raise ValueError("No headers found in the table")
    
    # Extract rows with improved validation
    rows = []
    data_rows = table.find_all('tr')[1:]  # Skip header row
    
    for tr in data_rows:
        row = []
        cells = tr.find_all(['td', 'th'])
        
        for cell in cells:
            # Clean cell text
            cell_text = cell.get_text().strip()
            # Remove footnote markers, citations, and normalize whitespace
            cell_text = re.sub(r'\[.*?\]', '', cell_text)
            cell_text = re.sub(r'\s+', ' ', cell_text)
            cell_text = cell_text.strip()
            row.append(cell_text)
        
        # FIX 2: Validate row length and handle mismatched columns
        if row:  # Skip completely empty rows
            # Pad short rows with empty strings
            while len(row) < len(headers):
                row.append('')
            
            # Truncate long rows to match header count
            if len(row) > len(headers):
                row = row[:len(headers)]
                
            rows.append(row)
    
    if not rows:
        raise ValueError("No data rows found in the table")
    
    # Create DataFrame
    df = pd.DataFrame(rows, columns=headers)
    return df

def clean_and_normalize_data_fixed(df):
    """
    Clean and normalize the scraped data with improved logic
    FIX 3: More selective data cleaning instead of blanket fillna
    """
    # Remove completely empty rows
    df = df.dropna(how='all')
    
    # Remove rows where all values are empty strings
    df = df[~(df == '').all(axis=1)]
    
    # More intelligent handling of missing data
    for column in df.columns:
        # For numeric-looking columns, try to preserve NaN for truly missing data
        if df[column].dtype == 'object':
            # Check if column contains mostly numeric data
            numeric_count = 0
            total_non_empty = 0
            
            for value in df[column]:
                if pd.notna(value) and str(value).strip():
                    total_non_empty += 1
                    # Check if it looks like a number
                    clean_val = re.sub(r'[^\d.,%-]', '', str(value))
                    if re.match(r'^[\d.,%-]+$', clean_val):
                        numeric_count += 1
            
            # If more than 70% of non-empty values look numeric, be more careful with filling
            if total_non_empty > 0 and numeric_count / total_non_empty > 0.7:
                # For numeric columns, only fill empty strings, keep NaN as is
                df[column] = df[column].replace('', pd.NA)
            else:
                # For text columns, fill with empty string
                df[column] = df[column].fillna('')
    
    return df

def save_data_fixed(df, csv_filename='table_data_fixed.csv', json_filename='table_data_fixed.json'):
    """
    Save DataFrame to CSV and JSON formats with better error handling
    """
    try:
        # Save as CSV
        df.to_csv(csv_filename, index=False, encoding='utf-8')
        
        # Save as JSON with better handling of NaN values
        data_dict = df.to_dict('records')
        
        # Clean up any remaining NaN values for JSON serialization
        cleaned_data = []
        for record in data_dict:
            cleaned_record = {}
            for key, value in record.items():
                if pd.isna(value):
                    cleaned_record[key] = None
                else:
                    cleaned_record[key] = value
            cleaned_data.append(cleaned_record)
        
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(cleaned_data, f, indent=2, ensure_ascii=False)
        
        print(f" Data saved successfully to {csv_filename} and {json_filename}")
        print(f" Table shape: {df.shape}")
        return df
        
    except Exception as e:
        print(f" Error saving data: {e}")
        raise

# Demo execution with the fixed version
def demo_fixed_scraper():
    """Demonstrate the fixed table scraper"""
    
    # Test with multiple Wikipedia pages
    test_urls = [
        ("https://en.wikipedia.org/wiki/List_of_programming_languages", 0, "Programming Languages List"),
        ("https://en.wikipedia.org/wiki/Comparison_of_programming_languages", 0, "Programming Languages Comparison"),
        ("https://en.wikipedia.org/wiki/Timeline_of_programming_languages", 0, "Programming Languages Timeline")
    ]
    
    for url, table_idx, description in test_urls:
        print(f"\n Testing: {description}")
        print(f"URL: {url}")
        print(f"Table index: {table_idx}")
        print("-" * 60)
        
        try:
            # Scrape the table
            df = scrape_wikipedia_table_fixed(url, table_index=table_idx)
            print(f" Successfully scraped table")
            print(f" Shape: {df.shape}")
            print(f" Columns: {list(df.columns)}")
            
            # Clean and normalize
            df_clean = clean_and_normalize_data_fixed(df)
            print(f" After cleaning: {df_clean.shape}")
            
            # Save data (with unique filenames)
            csv_name = f"table_data_fixed_{description.lower().replace(' ', '_')}.csv"
            json_name = f"table_data_fixed_{description.lower().replace(' ', '_')}.json"
            
            final_df = save_data_fixed(df_clean, csv_name, json_name)
            
            print(f"\n📄 First 3 records:")
            if len(final_df) > 0:
                print(final_df.head(3).to_string(index=False))
            else:
                print("No data to display")
                
            # Success - use this table for the main output
            save_data_fixed(df_clean, 'table_data_fixed.csv', 'table_data_fixed.json')
            return final_df
            
        except Exception as e:
            print(f" Failed: {e}")
            continue
    
    print(" All URLs failed to scrape successfully")
    return None

if __name__ == "__main__":
    result_df = demo_fixed_scraper()
