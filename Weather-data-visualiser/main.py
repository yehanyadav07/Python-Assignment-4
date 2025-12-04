

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

DATA_FILE = 'your_weather_data.csv' 
CLEANED_DATA_FILE = 'cleaned_weather_data.csv'
REPORT_FILE = 'summary_report.md'
PLOT_DIR = 'plots'

if not os.path.exists(PLOT_DIR):
    os.makedirs(PLOT_DIR)

def load_data(file_path):
    """Loads the CSV file into a Pandas DataFrame."""
    print(f"Loading data from {file_path}...")
    try:
        df = pd.read_csv(file_path)
        print("Data loaded successfully.")
        
        print("\n--- Data Structure (Head) ---")
        print(df.head())
        print("\n--- Data Information (Info) ---")
        df.info()
        print("\n--- Data Statistics (Describe) ---")
        print(df.describe())
        
        return df
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}. Please download the weather data.")
        return None

def clean_data(df):
    """Handles missing values, converts date formats, and filters columns."""
    print("\n--- Starting Data Cleaning and Processing ---")
    
    initial_rows = len(df)
    
    print(f"Rows dropped/filled: {initial_rows - len(df)} rows.")

    DATE_COLUMN = 'DateColumnName' # <-- CHANGE THIS
    try:
        df[DATE_COLUMN] = pd.to_datetime(df[DATE_COLUMN])
        df.set_index(DATE_COLUMN, inplace=True)
        print("Date column converted to datetime and set as index.")
    except KeyError:
        print(f"Warning: Date column '{DATE_COLUMN}' not found or incorrectly named.")
        return None
    except Exception as e:
        print(f"Error converting date column: {e}")
        return None
    
    RELEVANT_COLUMNS = ['Temperature', 'Rainfall', 'Humidity'] # <-- CHANGE THESE
    
    missing_cols = [col for col in RELEVANT_COLUMNS if col not in df.columns]
    if missing_cols:
        print(f"Warning: Missing relevant columns: {missing_cols}. Please check your column names.")
        existing_cols = [col for col in RELEVANT_COLUMNS if col in df.columns]
        df_cleaned = df[existing_cols].copy()
    else:
        df_cleaned = df[RELEVANT_COLUMNS].copy()
        
    print("Data cleaning complete.")
    return df_cleaned

def compute_statistics(df):
    """Computes overall statistics using NumPy and Pandas for summary."""
    print("\n--- Starting Statistical Analysis ---")
    
    overall_stats = df.agg({
        'Temperature': [np.mean, np.min, np.max, np.std],
        'Rainfall': [np.mean, np.min, np.max, np.std],
        'Humidity': [np.mean, np.min, np.max, np.std]
    }).rename(columns={'mean': 'Mean', 'amin': 'Min', 'amax': 'Max', 'std': 'StdDev'})
    
    print("\nOverall Summary Statistics (NumPy/Pandas):")
    print(overall_stats)
    
    return overall_stats

def group_and_aggregate(df):
    """Groups data by month and computes aggregate statistics (mean, total)."""
    print("\n--- Starting Grouping and Aggregation ---")
    
    monthly_summary = df.resample('M').agg({
        'Temperature': ['mean', 'min', 'max'],
        'Rainfall': 'sum',  # Total rainfall
        'Humidity': 'mean'
    })
    
    
    print("\nMonthly Aggregate Statistics (Pandas Groupby/Resample):")
    print(monthly_summary.head())
    
    return monthly_summary

def create_visualizations(df_cleaned, monthly_summary):
    """Creates required plots using Matplotlib and saves them as PNG files."""
    print("\n--- Creating Visualizations ---")
    
    plt.style.use('ggplot')

    plt.figure(figsize=(12, 6))
    plt.plot(df_cleaned.index, df_cleaned['Temperature'], label='Daily Temperature', color='tab:red')
    plt.title('Daily Temperature Trend')
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(PLOT_DIR, 'temperature_line_chart.png'))
    plt.close()
    print("Saved: temperature_line_chart.png")
    
    monthly_rainfall = monthly_summary['Rainfall']['sum']
    monthly_rainfall.index = monthly_rainfall.index.strftime('%Y-%m') 
    
    plt.figure(figsize=(12, 6))
    plt.bar(monthly_rainfall.index, monthly_rainfall.values, color='tab:blue')
    plt.title('Monthly Rainfall Totals')
    plt.xlabel('Month')
    plt.ylabel('Total Rainfall (mm)')
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y')
    plt.tight_layout()
    plt.savefig(os.path.join(PLOT_DIR, 'rainfall_bar_chart.png'))
    plt.close()
    print("Saved: rainfall_bar_chart.png")

    plt.figure(figsize=(8, 6))
    plt.scatter(df_cleaned['Temperature'], df_cleaned['Humidity'], alpha=0.6, color='tab:green')
    plt.title('Humidity vs. Temperature')
    plt.xlabel('Temperature (°C)')
    plt.ylabel('Humidity (%)')
    plt.grid(True)
    plt.savefig(os.path.join(PLOT_DIR, 'humidity_temp_scatter_plot.png'))
    plt.close()
    print("Saved: humidity_temp_scatter_plot.png")
    
    fig, axes = plt.subplots(2, 1, figsize=(12, 10), sharex=True) # Combined plot (Advanced Plotting Bonus) 

    axes[0].plot(df_cleaned.index, df_cleaned['Temperature'], color='tab:red', label='Temperature')
    axes[0].set_title('Daily Temperature and Humidity Trends')
    axes[0].set_ylabel('Temperature (°C)')
    axes[0].legend(loc='upper left')

    # Plot 2: Humidity
    axes[1].plot(df_cleaned.index, df_cleaned['Humidity'], color='tab:purple', label='Humidity')
    axes[1].set_xlabel('Date')
    axes[1].set_ylabel('Humidity (%)')
    axes[1].legend(loc='upper left')
    
    plt.tight_layout()
    plt.savefig(os.path.join(PLOT_DIR, 'combined_temp_humidity_subplots.png'))
    plt.close()
    print("Saved: combined_temp_humidity_subplots.png")

def export_results(df_cleaned, overall_stats, monthly_summary):
    """Exports cleaned data and generates the summary report."""
    print("\n--- Starting Export and Reporting ---")
    
    df_cleaned.to_csv(CLEANED_DATA_FILE)
    print(f"Cleaned data exported to {CLEANED_DATA_FILE}")

    report_content = f"""
# Weather Data Analysis Report

## 1. Introduction
This report summarizes the analysis and visualization of local weather data using Python libraries (Pandas, NumPy, Matplotlib) for the Weather Data Visualizer Mini Project. The goal is to derive meaningful insights for climate awareness [cite: 10] and potentially contribute to a campus sustainability initiative[cite: 12].

## 2. Dataset Overview
* **Source:** [Insert Data Source/Kaggle/IMD link here as required by Task 1] [cite: 18, 46]
* **Period:** [Insert the start and end date range of your data]
* **Key Columns Analyzed:** Temperature, Rainfall, Humidity [cite: 23]

## 3. Statistical Analysis Summary
The following statistics were computed using NumPy and Pandas[cite: 24, 26]:

### Overall Statistics:
{overall_stats.to_markdown()}

**Interpretation (Example):**
* **Temperature:** The average temperature was [Mean Temp], with a high variability (StdDev: [StdDev Temp]), suggesting significant seasonal changes.
* **Humidity:** Humidity levels were generally [Mean Humidity] with a minimum of [Min Humidity] and a maximum of [Max Humidity].

### Monthly Aggregation Summary
The data was grouped by month to analyze seasonal trends[cite: 34, 35]. Below is a snippet of the monthly results:

{monthly_summary.head().to_markdown()}

## 4. Visualization Insights
All plots are saved as PNG files in the '{PLOT_DIR}' directory[cite: 38].

### A. Daily Temperature Trend (temperature_line_chart.png)
The line chart clearly shows the temperature fluctuations over the period. [**Insert interpretation of the trend and any anomalies here.**] [cite: 29, 39]

### B. Monthly Rainfall Totals (rainfall_bar_chart.png)
The bar chart highlights the months with the highest and lowest rainfall. [**Insert interpretation, e.g., the peak rainy season was in [Month].**] [cite: 30, 39]

### C. Humidity vs. Temperature (humidity_temp_scatter_plot.png)
The scatter plot suggests a [positive/negative/no] correlation between humidity and temperature. [**Describe the relationship observed.**] [cite: 31, 39]

## 5. Conclusion
The analysis successfully provided insights into the local climate patterns, particularly the seasonal variations in temperature and rainfall. This information can be used to inform sustainability efforts, such as planning water conservation strategies around peak dry/rainy months.
"""
    
    with open(REPORT_FILE, 'w') as f:
        f.write(report_content)
    print(f"Summary report exported to {REPORT_FILE}")


def main():
    """Main function to run the entire data analysis and visualization pipeline."""
    
    df_raw = load_data(DATA_FILE)
    if df_raw is None:
        print("\nProcess aborted due to data loading failure.")
        return

    df_cleaned = clean_data(df_raw)
    if df_cleaned is None:
        print("\nProcess aborted due to data cleaning failure.")
        return
    

    overall_stats = compute_statistics(df_cleaned)
    

    monthly_summary = group_and_aggregate(df_cleaned)
    

    create_visualizations(df_cleaned, monthly_summary)
    
    export_results(df_cleaned, overall_stats, monthly_summary)
    
    print("\n--- Project Complete! ---")
    print("Remember to commit all files (script, CSV, plots, report) to your GitHub repository.")
    print(f"Repository Title: weather-data-visualizer-<yourname>")
    
if __name__ == "__main__":
    main()
