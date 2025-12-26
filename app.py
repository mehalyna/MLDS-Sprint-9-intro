"""
MLDS Sprint 9 - Data Acquisition and Preprocessing
Streamlit Visualization App

This app visualizes the results from all 6 data processing tasks:
- Task A: Table Scraping
- Task B: Weather Forecast & Anomaly Detection
- Task C: Normalize & Combine Weather Files
- Task D: Missing Data Imputation
- Task E: XML Parsing
- Task F: Free-text Weather Extraction
"""

import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys
import os

# Set page configuration
st.set_page_config(
    page_title="MLDS Sprint 9 - Data Visualization",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .task-header {
        font-size: 1.8rem;
        font-weight: bold;
        color: #2ca02c;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    .metric-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Helper functions
def load_json(filepath):
    """Load JSON file safely"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        st.error(f"Error decoding JSON from {filepath}")
        return None

def load_csv(filepath):
    """Load CSV file safely"""
    try:
        return pd.read_csv(filepath)
    except FileNotFoundError:
        return None
    except Exception as e:
        st.error(f"Error loading CSV from {filepath}: {e}")
        return None

def file_exists(filepath):
    """Check if file exists"""
    return Path(filepath).exists()

# Main app
def main():
    # Header
    st.markdown('<p class="main-header">📊 MLDS Sprint 9: Data Acquisition & Preprocessing</p>', 
                unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("🎯 Navigation")
    st.sidebar.markdown("---")
    
    task = st.sidebar.radio(
        "Select Task to Visualize:",
        [
            "🏠 Home",
            "📋 Task A: Table Scraping",
            "🌤️ Task B: Weather Forecast & Anomaly Detection",
            "🌍 Task C: Normalize & Combine Weather",
            "🔧 Task D: Missing Data Imputation",
            "📄 Task E: XML Parsing",
            "📝 Task F: Free-text Extraction"
        ]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.info("""
    **About this app:**
    
    This Streamlit application visualizes the results from 6 data processing tasks.
    
    Select a task from the menu to view its results and visualizations.
    """)
    
    # Main content based on selection
    if task == "🏠 Home":
        show_home()
    elif "Task A" in task:
        show_task_a()
    elif "Task B" in task:
        show_task_b()
    elif "Task C" in task:
        show_task_c()
    elif "Task D" in task:
        show_task_d()
    elif "Task E" in task:
        show_task_e()
    elif "Task F" in task:
        show_task_f()

def show_home():
    """Display home page with overview"""
    st.markdown('<p class="task-header">Welcome to Data Visualization Dashboard</p>', 
                unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### 📚 Project Overview
        
        This dashboard visualizes the results from six data acquisition and preprocessing tasks:
        
        **Task A: Table Scraping** 📋
        - Scrape Wikipedia tables
        - Clean and normalize data
        - Export to CSV/JSON
        
        **Task B: Weather Forecast & Anomaly Detection** 🌤️
        - Fetch 7-day forecasts from API
        - Detect temperature anomalies
        - Statistical analysis (mean, std)
        
        **Task C: Normalize & Combine Weather** 🌍
        - Handle multiple data schemas
        - Normalize date formats
        - Combine multi-city data
        
        **Task D: Missing Data Imputation** 🔧
        - Detect missing values
        - Linear interpolation
        - Moving average imputation
        
        **Task E: XML Parsing** 📄
        - Parse XML with namespaces
        - Extract hourly weather data
        - Find peak temperatures
        
        **Task F: Free-text Extraction** 📝
        - Extract data from text logs
        - Multi-language pattern matching
        - Temperature unit conversion
        """)
    
    with col2:
        st.markdown("### 📊 Quick Stats")
        
        # Check which output files exist
        files_status = {
            "Task A": file_exists("table_data.csv"),
            "Task B": file_exists("weekly_summary.json"),
            "Task C": file_exists("cities_comparison.csv"),
            "Task D": file_exists("imputation_report_buggy.json"),
            "Task E": file_exists("normalized_hourly.json"),
            "Task F": file_exists("extracted_weather_data_buggy.csv")
        }
        
        completed = sum(files_status.values())
        total = len(files_status)
        
        st.metric("Tasks with Output", f"{completed}/{total}")
        
        st.markdown("### 📁 Output Files Status")
        for task, exists in files_status.items():
            status = "✅" if exists else "⚠️"
            st.markdown(f"{status} {task}")
        
        if completed < total:
            st.warning("⚠️ Some tasks haven't generated output files yet. Run the examples to see complete visualizations.")
        else:
            st.success("✅ All tasks have generated output files!")

def show_task_a():
    """Visualize Task A: Table Scraping results"""
    st.markdown('<p class="task-header">📋 Task A: Table Scraping</p>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    **Objective:** Scrape structured data from Wikipedia tables and convert to CSV/JSON.
    """)
    
    # Load data
    df = load_csv("table_data.csv")
    json_data = load_json("table_data.json")
    
    if df is not None:
        # Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Records", len(df))
        with col2:
            st.metric("Columns", len(df.columns))
        with col3:
            st.metric("Data Size", f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB")
        
        # Display options
        st.markdown("---")
        view_option = st.radio("View Mode:", ["Table View", "JSON View", "Statistics"])
        
        if view_option == "Table View":
            st.subheader("📊 Scraped Table Data")
            
            # Search and filter
            search = st.text_input("🔍 Search in table:", "")
            if search:
                mask = df.astype(str).apply(lambda x: x.str.contains(search, case=False, na=False)).any(axis=1)
                filtered_df = df[mask]
                st.info(f"Found {len(filtered_df)} matching records")
                st.dataframe(filtered_df, use_container_width=True)
            else:
                st.dataframe(df, use_container_width=True)
            
            # Download button
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name="scraped_table_data.csv",
                mime="text/csv"
            )
        
        elif view_option == "JSON View":
            st.subheader("📄 JSON Structure")
            if json_data:
                st.json(json_data[:3] if len(json_data) > 3 else json_data)
                st.info(f"Showing first 3 records out of {len(json_data)} total")
            else:
                st.warning("JSON file not found")
        
        else:  # Statistics
            st.subheader("📈 Data Statistics")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Column Information:**")
                for col in df.columns:
                    non_null = df[col].notna().sum()
                    null_count = df[col].isna().sum()
                    st.write(f"**{col}:** {non_null} non-null, {null_count} null")
            
            with col2:
                st.markdown("**Data Quality:**")
                total_cells = df.size
                non_null_cells = df.notna().sum().sum()
                completeness = (non_null_cells / total_cells) * 100
                
                st.write(f"**Total Cells:** {total_cells:,}")
                st.write(f"**Non-null Cells:** {non_null_cells:,}")
                st.write(f"**Completeness:** {completeness:.1f}%")
                
                # Completeness gauge
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=completeness,
                    title={'text': "Data Completeness"},
                    gauge={'axis': {'range': [None, 100]},
                           'bar': {'color': "darkblue"},
                           'steps': [
                               {'range': [0, 50], 'color': "lightgray"},
                               {'range': [50, 80], 'color': "gray"},
                               {'range': [80, 100], 'color': "lightgreen"}],
                           'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 90}}
                ))
                fig.update_layout(height=250)
                st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ No data found. Please run `examples_py/example1.py` to generate the output files.")
        st.info("Run: `python examples_py/example1.py`")

def show_task_b():
    """Visualize Task B: Weather Forecast & Anomaly Detection"""
    st.markdown('<p class="task-header">🌤️ Task B: Weather Forecast & Anomaly Detection</p>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    **Objective:** Fetch 7-day weather forecasts and detect temperature anomalies using statistical methods.
    """)
    
    # Load data
    summary = load_json("weekly_summary.json")
    summary_fixed = load_json("weekly_summary_fixed.json")
    
    if summary:
        # Display version selector
        version = st.radio("Select Version:", ["Buggy Version", "Fixed Version"])
        data = summary_fixed if version == "Fixed Version" and summary_fixed else summary
        
        # Metrics
        st.markdown("### 📊 Statistical Summary")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Mean Temperature",
                f"{data.get('mean', 0):.2f}°C",
                help="Average temperature over 7 days"
            )
        
        with col2:
            st.metric(
                "Standard Deviation",
                f"{data.get('std', 0):.2f}°C",
                help="Temperature variability measure"
            )
        
        with col3:
            anomaly_count = len(data.get('anomalies', []))
            st.metric(
                "Anomalies Detected",
                anomaly_count,
                help="Days with temperatures beyond ±2σ threshold"
            )
        
        # Anomaly details
        if data.get('anomalies'):
            st.markdown("---")
            st.subheader("🚨 Detected Anomalies")
            
            anomalies_df = pd.DataFrame({
                'Date': data['anomalies'],
                'Status': ['⚠️ Anomaly'] * len(data['anomalies'])
            })
            st.dataframe(anomalies_df, use_container_width=True, hide_index=True)
        else:
            st.success("✅ No anomalies detected - all temperatures within normal range!")
        
        # Threshold visualization
        st.markdown("---")
        st.subheader("📈 Anomaly Detection Method")
        
        mean = data.get('mean', 0)
        std = data.get('std', 0)
        threshold = data.get('threshold', 2 * std)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Create threshold visualization
            temps = [mean - threshold, mean, mean + threshold]
            labels = ['Lower Threshold', 'Mean', 'Upper Threshold']
            
            fig = go.Figure()
            
            # Add range area
            fig.add_trace(go.Scatter(
                x=['Day 1', 'Day 7'],
                y=[mean + threshold, mean + threshold],
                fill=None,
                mode='lines',
                line=dict(color='red', dash='dash'),
                name='Upper Threshold',
                showlegend=True
            ))
            
            fig.add_trace(go.Scatter(
                x=['Day 1', 'Day 7'],
                y=[mean - threshold, mean - threshold],
                fill='tonexty',
                mode='lines',
                line=dict(color='red', dash='dash'),
                name='Lower Threshold',
                fillcolor='rgba(255, 0, 0, 0.1)',
                showlegend=True
            ))
            
            fig.add_trace(go.Scatter(
                x=['Day 1', 'Day 7'],
                y=[mean, mean],
                mode='lines',
                line=dict(color='blue', width=2),
                name='Mean Temperature'
            ))
            
            fig.update_layout(
                title="Temperature Thresholds for Anomaly Detection",
                xaxis_title="Time Period",
                yaxis_title="Temperature (°C)",
                height=400,
                showlegend=True
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("**Detection Method:**")
            st.write(f"• Mean (μ): {mean:.2f}°C")
            st.write(f"• Std Dev (σ): {std:.2f}°C")
            st.write(f"• Threshold: ±{threshold:.2f}°C")
            st.write(f"• Method: 2-sigma rule")
            
            st.markdown("**Formula:**")
            st.latex(r"\text{Anomaly if: } |T - \mu| > 2\sigma")
        
        # Raw JSON view
        with st.expander("🔍 View Raw JSON Data"):
            st.json(data)
    
    else:
        st.warning("⚠️ No data found. Please run `examples_py/example2.py` to generate the output files.")
        st.info("Run: `python examples_py/example2.py`")

def show_task_c():
    """Visualize Task C: Normalize & Combine Weather Files"""
    st.markdown('<p class="task-header">🌍 Task C: Normalize & Combine Weather</p>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    **Objective:** Normalize weather data from multiple cities with different JSON schemas into unified format.
    """)
    
    # Load data
    df = load_csv("cities_comparison.csv")
    df_fixed = load_csv("cities_comparison_fixed.csv")
    
    if df is not None or df_fixed is not None:
        # Version selector
        version = st.radio("Select Version:", ["Buggy Version", "Fixed Version"])
        data = df_fixed if version == "Fixed Version" and df_fixed is not None else df
        
        if data is not None:
            # Metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Records", len(data))
            with col2:
                st.metric("Cities", data['city'].nunique())
            with col3:
                st.metric("Date Range", f"{len(data['date'].unique())} days")
            with col4:
                completeness = (data.notna().sum().sum() / data.size) * 100
                st.metric("Completeness", f"{completeness:.1f}%")
            
            # Data view
            st.markdown("---")
            st.subheader("📊 Combined Weather Data")
            
            # Filter by city
            cities = ['All'] + sorted(data['city'].unique().tolist())
            selected_city = st.selectbox("Filter by City:", cities)
            
            if selected_city != 'All':
                filtered_data = data[data['city'] == selected_city]
            else:
                filtered_data = data
            
            st.dataframe(filtered_data, use_container_width=True, hide_index=True)
            
            # Visualizations
            st.markdown("---")
            st.subheader("📈 Weather Comparisons")
            
            tab1, tab2, tab3 = st.tabs(["🌡️ Temperature", "💧 Precipitation", "💨 Wind & Humidity"])
            
            with tab1:
                # Temperature comparison
                fig = go.Figure()
                
                for city in data['city'].unique():
                    city_data = data[data['city'] == city]
                    fig.add_trace(go.Scatter(
                        x=city_data['date'],
                        y=city_data['max'],
                        name=f"{city} (Max)",
                        mode='lines+markers'
                    ))
                    fig.add_trace(go.Scatter(
                        x=city_data['date'],
                        y=city_data['min'],
                        name=f"{city} (Min)",
                        mode='lines+markers',
                        line=dict(dash='dash')
                    ))
                
                fig.update_layout(
                    title="Temperature Comparison by City",
                    xaxis_title="Date",
                    yaxis_title="Temperature (°C)",
                    height=500,
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with tab2:
                # Precipitation comparison
                fig = px.bar(
                    data,
                    x='date',
                    y='precip',
                    color='city',
                    title="Precipitation by City",
                    labels={'precip': 'Precipitation (mm)', 'date': 'Date'},
                    barmode='group'
                )
                fig.update_layout(height=500)
                st.plotly_chart(fig, use_container_width=True)
            
            with tab3:
                col1, col2 = st.columns(2)
                
                with col1:
                    # Wind speed
                    fig = px.line(
                        data,
                        x='date',
                        y='wind',
                        color='city',
                        title="Wind Speed by City",
                        labels={'wind': 'Wind Speed (km/h)', 'date': 'Date'}
                    )
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Humidity
                    fig = px.line(
                        data,
                        x='date',
                        y='humidity',
                        color='city',
                        title="Humidity by City",
                        labels={'humidity': 'Humidity (%)', 'date': 'Date'}
                    )
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
            
            # Summary statistics
            st.markdown("---")
            st.subheader("📊 Summary Statistics by City")
            
            summary_stats = data.groupby('city').agg({
                'max': ['mean', 'min', 'max'],
                'min': ['mean', 'min', 'max'],
                'precip': 'sum',
                'wind': 'mean',
                'humidity': 'mean'
            }).round(2)
            
            st.dataframe(summary_stats, use_container_width=True)
    
    else:
        st.warning("⚠️ No data found. Please run `examples_py/example3.py` to generate the output files.")
        st.info("Run: `python examples_py/example3.py`")

def show_task_d():
    """Visualize Task D: Missing Data Imputation"""
    st.markdown('<p class="task-header">🔧 Task D: Missing Data Imputation</p>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    **Objective:** Detect missing values and implement imputation strategies (linear interpolation & moving average).
    """)
    
    # Load data
    report_buggy = load_json("imputation_report_buggy.json")
    report_fixed = load_json("imputation_report_fixed.json")
    imputed_data = load_json("tokyo_imputed_buggy.json")
    imputed_fixed = load_json("tokyo_imputed_fixed.json")
    
    if report_buggy or report_fixed:
        # Version selector
        version = st.radio("Select Version:", ["Buggy Version", "Fixed Version"])
        report = report_fixed if version == "Fixed Version" and report_fixed else report_buggy
        data = imputed_fixed if version == "Fixed Version" and imputed_fixed else imputed_data
        
        # Imputation counts
        st.markdown("### 📊 Imputation Summary")
        
        if report:
            counts = report.get('imputed_counts', {})
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Max Temp Imputed", counts.get('temp_max', 0))
            with col2:
                st.metric("Min Temp Imputed", counts.get('temp_min', 0))
            with col3:
                st.metric("Humidity Imputed", counts.get('humidity', 0))
            with col4:
                st.metric("Wind Speed Imputed", counts.get('wind_speed', 0))
            
            # Imputation methods
            if 'strategies_used' in report:
                st.markdown("---")
                st.subheader("🔍 Imputation Strategies Used")
                
                strategies = report['strategies_used']
                st.markdown(f"""
                - **Temperature (max/min):** `{strategies.get('temp_max', 'N/A')}` / `{strategies.get('temp_min', 'N/A')}`
                - **Humidity:** `{strategies.get('humidity', 'N/A')}`
                - **Wind Speed:** `{strategies.get('wind_speed', 'N/A')}`
                """)
            
            # Visualization of imputation counts
            st.markdown("---")
            st.subheader("📈 Imputation Counts by Field")
            
            fig = px.bar(
                x=list(counts.keys()),
                y=list(counts.values()),
                labels={'x': 'Field', 'y': 'Count'},
                title="Number of Values Imputed per Field",
                color=list(counts.values()),
                color_continuous_scale='Blues'
            )
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        # Show imputed data
        if data:
            st.markdown("---")
            st.subheader("📋 Imputed Weather Data")
            
            weather_data = data.get('weather_data', [])
            if weather_data:
                df = pd.DataFrame(weather_data)
                
                # Display table
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                # Visualize imputed data
                st.markdown("---")
                st.subheader("📊 Weather Data After Imputation")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Temperature plot
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=df['date'],
                        y=df['temp_max'],
                        name='Max Temperature',
                        mode='lines+markers'
                    ))
                    fig.add_trace(go.Scatter(
                        x=df['date'],
                        y=df['temp_min'],
                        name='Min Temperature',
                        mode='lines+markers'
                    ))
                    fig.update_layout(
                        title="Temperature After Imputation",
                        xaxis_title="Date",
                        yaxis_title="Temperature (°C)",
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Humidity & Wind plot
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=df['date'],
                        y=df['humidity'],
                        name='Humidity',
                        yaxis='y',
                        mode='lines+markers'
                    ))
                    fig.add_trace(go.Scatter(
                        x=df['date'],
                        y=df['wind_speed'],
                        name='Wind Speed',
                        yaxis='y2',
                        mode='lines+markers'
                    ))
                    fig.update_layout(
                        title="Humidity & Wind Speed After Imputation",
                        xaxis_title="Date",
                        yaxis=dict(title="Humidity (%)", side='left'),
                        yaxis2=dict(title="Wind Speed (km/h)", overlaying='y', side='right'),
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
        
        # Method explanation
        with st.expander("📚 Learn About Imputation Methods"):
            st.markdown("""
            ### Linear Interpolation
            Used for temperature data. Finds the nearest valid values before and after a missing value and calculates 
            the missing value using linear interpolation:
            
            ```
            value = y1 + (y2 - y1) * (x - x1) / (x2 - x1)
            ```
            
            ### Moving Average
            Used for humidity and wind speed. Calculates the mean of valid values within a sliding window around 
            the missing value:
            
            ```
            value = mean(valid_values_in_window)
            ```
            """)
    
    else:
        st.warning("⚠️ No data found. Please run `examples_py/example4.py` to generate the output files.")
        st.info("Run: `python examples_py/example4.py`")

def show_task_e():
    """Visualize Task E: XML Parsing"""
    st.markdown('<p class="task-header">📄 Task E: XML Parsing</p>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    **Objective:** Parse XML files with namespaces to extract hourly weather data and find peak temperatures.
    """)
    
    # Load data
    hourly_data = load_json("normalized_hourly.json")
    peak_hours = load_csv("peak_hours.csv")
    
    if hourly_data:
        # Summary metrics
        st.markdown("### 📊 Parsing Summary")
        
        total_days = len(hourly_data)
        total_hours = sum(len(day.get('hourly', [])) for day in hourly_data)
        avg_hours = total_hours / total_days if total_days > 0 else 0
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Days Parsed", total_days)
        with col2:
            st.metric("Total Hourly Records", total_hours)
        with col3:
            st.metric("Avg Hours per Day", f"{avg_hours:.1f}")
        
        # Display hourly data
        st.markdown("---")
        st.subheader("🕐 Hourly Weather Data")
        
        # Day selector
        dates = [day['date'] for day in hourly_data]
        selected_date = st.selectbox("Select Date:", dates)
        
        # Find selected day data
        selected_day = next((day for day in hourly_data if day['date'] == selected_date), None)
        
        if selected_day and selected_day.get('hourly'):
            hourly_df = pd.DataFrame(selected_day['hourly'])
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown("**Hourly Data Table:**")
                st.dataframe(hourly_df, use_container_width=True, hide_index=True)
            
            with col2:
                # Plot hourly temperatures
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=hourly_df['time'],
                    y=hourly_df['temperature'],
                    name='Temperature',
                    mode='lines+markers',
                    line=dict(color='red', width=2),
                    marker=dict(size=8)
                ))
                
                # Add wind speed on secondary axis
                fig.add_trace(go.Scatter(
                    x=hourly_df['time'],
                    y=hourly_df['wind_speed'],
                    name='Wind Speed',
                    mode='lines+markers',
                    line=dict(color='blue', width=2, dash='dash'),
                    marker=dict(size=8),
                    yaxis='y2'
                ))
                
                fig.update_layout(
                    title=f"Hourly Weather Data for {selected_date}",
                    xaxis_title="Time",
                    yaxis=dict(title="Temperature (°C)", side='left'),
                    yaxis2=dict(title="Wind Speed (km/h)", overlaying='y', side='right'),
                    height=500,
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No hourly data available for this date")
    
    # Peak hours
    if peak_hours is not None:
        st.markdown("---")
        st.subheader("🏔️ Peak Temperature Hours")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.dataframe(peak_hours, use_container_width=True, hide_index=True)
        
        with col2:
            # Plot peak temperatures
            fig = px.bar(
                peak_hours,
                x='date',
                y='peak_temp',
                title="Peak Temperatures by Day",
                labels={'peak_temp': 'Peak Temperature (°C)', 'date': 'Date'},
                text='peak_hour',
                color='peak_temp',
                color_continuous_scale='Reds'
            )
            fig.update_traces(texttemplate='%{text}', textposition='outside')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    # XML structure info
    with st.expander("🔍 XML Structure Information"):
        st.markdown("""
        ### XML Namespace Handling
        
        The XML file uses two namespaces:
        - **Default namespace:** `http://weather.example.com/default`
        - **Weather namespace (w:):** `http://weather.example.com/schema`
        
        ### Structure:
        ```xml
        <weather xmlns:w="..." xmlns="...">
            <day date="2024-08-18">
                <hour time="00:00">
                    <w:temp>22.1</w:temp>
                    <w:wind>12.5</w:wind>
                </hour>
            </day>
        </weather>
        ```
        """)
    
    if not hourly_data and not peak_hours:
        st.warning("⚠️ No data found. Please run `examples_py/example5.py` to generate the output files.")
        st.info("Run: `python examples_py/example5.py`")

def show_task_f():
    """Visualize Task F: Free-text Extraction"""
    st.markdown('<p class="task-header">📝 Task F: Free-text Weather Extraction</p>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    **Objective:** Extract structured weather data from free-text logs using regular expressions.
    """)
    
    # Load data
    df = load_csv("extracted_weather_data_buggy.csv")
    df_fixed = load_csv("extracted_weather_data_fixed.csv")
    
    # Load patterns
    patterns = None
    try:
        with open("patterns_buggy.txt", 'r', encoding='utf-8') as f:
            patterns = f.read()
    except:
        pass
    
    if df is not None or df_fixed is not None:
        # Version selector
        version = st.radio("Select Version:", ["Buggy Version", "Fixed Version"])
        data = df_fixed if version == "Fixed Version" and df_fixed is not None else df
        
        if data is not None:
            # Metrics
            st.markdown("### 📊 Extraction Summary")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Records Extracted", len(data))
            with col2:
                valid_dates = data['Date'].notna().sum()
                st.metric("Valid Dates", f"{valid_dates}/{len(data)}")
            with col3:
                valid_temps = data['Max Temperature'].notna().sum()
                st.metric("Valid Temperatures", f"{valid_temps}/{len(data)}")
            with col4:
                completeness = (data.notna().sum().sum() / data.size) * 100
                st.metric("Completeness", f"{completeness:.1f}%")
            
            # Data view
            st.markdown("---")
            st.subheader("📋 Extracted Weather Data")
            
            # Clean up display
            display_df = data.copy()
            st.dataframe(display_df, use_container_width=True, hide_index=True)
            
            # Visualizations
            st.markdown("---")
            st.subheader("📈 Extracted Data Visualizations")
            
            tab1, tab2, tab3 = st.tabs(["🌡️ Temperatures", "💧 Humidity & Precipitation", "📊 Data Quality"])
            
            with tab1:
                # Temperature comparison
                fig = go.Figure()
                
                valid_data = data.dropna(subset=['Max Temperature', 'Min Temperature'])
                
                fig.add_trace(go.Scatter(
                    x=valid_data['Date'],
                    y=valid_data['Max Temperature'],
                    name='Max Temperature',
                    mode='lines+markers',
                    line=dict(color='red')
                ))
                
                fig.add_trace(go.Scatter(
                    x=valid_data['Date'],
                    y=valid_data['Min Temperature'],
                    name='Min Temperature',
                    mode='lines+markers',
                    line=dict(color='blue')
                ))
                
                fig.update_layout(
                    title="Extracted Temperatures",
                    xaxis_title="Date",
                    yaxis_title="Temperature (°C)",
                    height=500
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with tab2:
                col1, col2 = st.columns(2)
                
                with col1:
                    # Humidity
                    valid_humidity = data.dropna(subset=['Humidity'])
                    fig = px.bar(
                        valid_humidity,
                        x='Date',
                        y='Humidity',
                        title="Extracted Humidity Values",
                        labels={'Humidity': 'Humidity (%)'}
                    )
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Precipitation
                    valid_precip = data.dropna(subset=['Precipitation'])
                    fig = px.bar(
                        valid_precip,
                        x='Date',
                        y='Precipitation',
                        title="Extracted Precipitation Values",
                        labels={'Precipitation': 'Precipitation (mm)'},
                        color='Precipitation',
                        color_continuous_scale='Blues'
                    )
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
            
            with tab3:
                # Data quality visualization
                st.markdown("**Field Completeness:**")
                
                completeness_data = {
                    'Field': data.columns.tolist(),
                    'Valid': [data[col].notna().sum() for col in data.columns],
                    'Missing': [data[col].isna().sum() for col in data.columns]
                }
                completeness_df = pd.DataFrame(completeness_data)
                completeness_df['Percentage'] = (completeness_df['Valid'] / len(data) * 100).round(1)
                
                fig = px.bar(
                    completeness_df,
                    x='Field',
                    y='Percentage',
                    title="Data Extraction Success Rate by Field",
                    labels={'Percentage': 'Success Rate (%)'},
                    text='Percentage',
                    color='Percentage',
                    color_continuous_scale='Greens'
                )
                fig.update_traces(texttemplate='%{text}%', textposition='outside')
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
                
                st.dataframe(completeness_df, use_container_width=True, hide_index=True)
        
        # Show regex patterns
        if patterns:
            with st.expander("🔍 View Regex Patterns Used"):
                st.code(patterns, language='text')
    
    else:
        st.warning("⚠️ No data found. Please run `examples_py/example6.py` to generate the output files.")
        st.info("Run: `python examples_py/example6.py`")

# Run the app
if __name__ == "__main__":
    main()
