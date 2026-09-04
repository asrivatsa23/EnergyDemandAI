"""
Generate Additional Indian Power Grid Datasets
===============================================
Generates raw datasets in data/raw/ for electricity demand, weather variables,
and holiday/festival metadata across Indian Power Grid regions.
"""

import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_datasets():
    np.random.seed(101)

    raw_elec_dir = os.path.join("data", "raw", "electricity")
    raw_weather_dir = os.path.join("data", "raw", "weather")
    raw_holiday_dir = os.path.join("data", "raw", "holidays")

    for d in [raw_elec_dir, raw_weather_dir, raw_holiday_dir]:
        os.makedirs(d, exist_ok=True)

    # 1. Indian Holidays Dataset (2023-2025)
    holidays = [
        {"Date": "2023-01-26", "Holiday_Name": "Republic Day", "Type": "National", "Grid_Impact": "High"},
        {"Date": "2023-03-08", "Holiday_Name": "Holi", "Type": "Festival", "Grid_Impact": "Medium"},
        {"Date": "2023-08-15", "Holiday_Name": "Independence Day", "Type": "National", "Grid_Impact": "High"},
        {"Date": "2023-10-02", "Holiday_Name": "Gandhi Jayanti", "Type": "National", "Grid_Impact": "Medium"},
        {"Date": "2023-10-24", "Holiday_Name": "Dussehra", "Type": "Festival", "Grid_Impact": "Medium"},
        {"Date": "2023-11-12", "Holiday_Name": "Diwali", "Type": "Festival", "Grid_Impact": "High"},
        {"Date": "2023-12-25", "Holiday_Name": "Christmas", "Type": "Festival", "Grid_Impact": "Medium"},
        {"Date": "2024-01-26", "Holiday_Name": "Republic Day", "Type": "National", "Grid_Impact": "High"},
        {"Date": "2024-03-25", "Holiday_Name": "Holi", "Type": "Festival", "Grid_Impact": "Medium"},
        {"Date": "2024-08-15", "Holiday_Name": "Independence Day", "Type": "National", "Grid_Impact": "High"},
        {"Date": "2024-10-02", "Holiday_Name": "Gandhi Jayanti", "Type": "National", "Grid_Impact": "Medium"},
        {"Date": "2024-11-01", "Holiday_Name": "Diwali", "Type": "Festival", "Grid_Impact": "High"},
        {"Date": "2025-01-26", "Holiday_Name": "Republic Day", "Type": "National", "Grid_Impact": "High"},
        {"Date": "2025-08-15", "Holiday_Name": "Independence Day", "Type": "National", "Grid_Impact": "High"},
        {"Date": "2025-10-20", "Holiday_Name": "Diwali", "Type": "Festival", "Grid_Impact": "High"}
    ]
    df_holidays = pd.DataFrame(holidays)
    holiday_path = os.path.join(raw_holiday_dir, "indian_holidays_2023_2025.csv")
    df_holidays.to_csv(holiday_path, index=False)
    print(f"Generated Indian Holidays Dataset: {holiday_path}")

    # 2. Regional Demand Dataset (2023-2024 hourly)
    start_date = datetime(2023, 1, 1)
    hours = 365 * 24
    timestamps = [start_date + timedelta(hours=i) for i in range(hours)]

    regions = ["Northern Region", "Western Region", "Southern Region", "Eastern Region", "North-Eastern Region"]
    regional_records = []

    for ts in timestamps:
        hour = ts.hour
        month = ts.month
        
        for reg in regions:
            base = 450.0 if reg == "Western Region" else (400.0 if reg in ["Northern Region", "Southern Region"] else 200.0)
            mult = 1.0 + 0.2 * np.sin((hour - 8) * np.pi / 12) + (0.15 if month in [5, 6] else 0.0)
            demand_mu = round(max(50.0, base * mult + np.random.normal(0, 15)), 2)
            peak_mw = round(demand_mu * 18.2 + np.random.normal(0, 30), 1)

            regional_records.append({
                "Datetime": ts.strftime("%Y-%m-%d %H:00:00"),
                "Region": reg,
                "Energy Required (MU)": demand_mu,
                "Peak Demand (MW)": peak_mw,
                "Grid Frequency (Hz)": round(50.0 + np.random.normal(0, 0.04), 2)
            })

    df_reg = pd.DataFrame(regional_records)
    reg_path = os.path.join(raw_elec_dir, "india_regional_demand_2023_2024.csv")
    df_reg.to_csv(reg_path, index=False)
    print(f"Generated Regional Demand Dataset: {reg_path} ({len(df_reg)} rows)")

    # 3. Weather Dataset across major Indian metropolitan centers
    weather_records = []
    cities = [("Mumbai", "Western Region"), ("Delhi", "Northern Region"), ("Chennai", "Southern Region"), ("Kolkata", "Eastern Region")]

    for ts in timestamps:
        month = ts.month
        hour = ts.hour
        for city, reg in cities:
            base_temp = 32.0 if month in [4, 5, 6] else (20.0 if month in [12, 1] else 27.0)
            temp = round(base_temp + 4.0 * np.sin((hour - 8) * np.pi / 12) + np.random.normal(0, 1), 1)
            humidity = round(float(np.clip(60.0 + np.random.normal(0, 10), 30, 95)), 1)
            rainfall = round(max(0.0, float(np.random.exponential(1.2) if month in [6,7,8,9] and np.random.rand() < 0.2 else 0.0)), 1)

            weather_records.append({
                "Datetime": ts.strftime("%Y-%m-%d %H:00:00"),
                "City": city,
                "Region": reg,
                "Temperature (°C)": temp,
                "Humidity (%)": humidity,
                "Rainfall (mm)": rainfall
            })

    df_weather = pd.DataFrame(weather_records)
    weather_path = os.path.join(raw_weather_dir, "india_regional_weather_2023_2024.csv")
    df_weather.to_csv(weather_path, index=False)
    print(f"Generated Regional Weather Dataset: {weather_path} ({len(df_weather)} rows)")

if __name__ == "__main__":
    generate_datasets()
