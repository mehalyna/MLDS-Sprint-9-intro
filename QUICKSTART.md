# Quick Start Guide

## Getting Started with MLDS Sprint 9

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Interactive Dashboard

```bash
streamlit run app.py
```

The dashboard will automatically open in your browser at `http://localhost:8501`

### Generate Output Files (Optional)

If you want to regenerate the output files, run any example:

```bash
# Run all examples at once (PowerShell)
foreach ($i in 1..6) { python examples_py/example$i.py }

# Or run individually
python examples_py/example1.py  # Task A
python examples_py/example2.py  # Task B
python examples_py/example3.py  # Task C
python examples_py/example4.py  # Task D
python examples_py/example5.py  # Task E
python examples_py/example6.py  # Task F
```

---

## Dashboard Features

The Streamlit dashboard provides:

### Home Page
- Overview of all tasks
- Quick stats on completed tasks
- Status of output files

### Task A: Table Scraping
- View scraped Wikipedia tables
- Search and filter data
- Download as CSV
- Data quality metrics

### Task B: Weather Forecast & Anomaly Detection
- Statistical summary (mean, std dev)
- Anomaly detection visualization
- Threshold explanations
- Compare buggy vs fixed versions

### Task C: Normalize & Combine Weather
- Multi-city weather comparison
- Interactive temperature charts
- Precipitation and wind visualizations
- Summary statistics by city

### Task D: Missing Data Imputation
- Imputation counts by field
- Before/after visualizations
- Strategy explanations
- Data completeness metrics

### Task E: XML Parsing
- Hourly weather data viewer
- Peak temperature analysis
- Interactive time-series charts
- Day-by-day exploration

### Task F: Free-text Extraction
- Extracted weather data tables
- Temperature trends
- Data quality analysis
- Regex pattern viewer

---

## Navigation Tips

1. **Use the sidebar** to switch between tasks
2. **Toggle versions** to compare buggy vs fixed implementations
3. **Hover over charts** for detailed information
4. **Expand sections** to learn about methods and algorithms
5. **Download data** directly from the dashboard

---

## Troubleshooting

### "No data found" warning?
Run the corresponding Python script to generate the output files:
```bash
python examples_py/example1.py
```

### Port already in use?
Specify a different port:
```bash
streamlit run app.py --server.port 8502
```

### Missing dependencies?
Reinstall all requirements:
```bash
pip install -r requirements.txt --upgrade
```

---

## Learn More

- Read the full [README.md](README.md) for detailed task descriptions
- Explore the [examples_py/](examples_py/) folder for Python implementations
- Check out the [examples_ipynb/](examples_ipynb/) folder for Jupyter notebooks

---

## Features Coming Soon

- [ ] Export all visualizations as images
- [ ] Batch processing multiple files
- [ ] Real-time data streaming
- [ ] Custom data upload
- [ ] Advanced filtering options

---

**Happy Data Processing!**
