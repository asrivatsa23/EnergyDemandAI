"""
Generate Realistic Indian Electricity Demand Sample Dataset
==========================================================
Produces hourly Indian electricity grid dataset with state/region metadata,
weather variables, renewable generation (solar, wind, hydro), and holidays/festivals.
"""

import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_indian_electricity_dataset():
    np.random.seed(42)

    # 1 Year hourly range
    start_date = datetime(2023, 1, 1, 0, 0, 0)
    hours = 365 * 24
    timestamps = [start_date + timedelta(hours=i) for i in range(hours)]

    regions_states = [
        ("Western Region", "Maharashtra"),
        ("Western Region", "Gujarat"),
        ("Southern Region", "Tamil Nadu"),
        ("Southern Region", "Karnataka"),
        ("Northern Region", "Delhi"),
        ("Northern Region", "Uttar Pradesh"),
        ("Eastern Region", "West Bengal")
    ]

    records = []

    # Indian Holidays & Festivals dates (2023)
    indian_holidays = {
        "2023-01-26": "Republic Day",
        "2023-03-08": "Holi",
        "2023-08-15": "Independence Day",
        "2023-10-02": "Gandhi Jayanti",
        "2023-10-24": "Dussehra",
        "2023-11-12": "Diwali",
        "2023-12-25": "Christmas"
    }

    for ts in timestamps:
        date_str = ts.strftime("%Y-%m-%d")
        hour = ts.hour
        month = ts.month
        day_of_week = ts.weekday()

        # Seasonal base temperature in India (Degrees C)
        # Summer (Apr-Jul): 30-42°C, Winter (Dec-Feb): 10-22°C, Monsoon (Jul-Sep): 25-32°C
        if month in [4, 5, 6, 7]:
            base_temp = 34.0 + 5.0 * np.sin((hour - 8) * np.pi / 12)
        elif month in [12, 1, 2]:
            base_temp = 18.0 + 4.0 * np.sin((hour - 8) * np.pi / 12)
        else:
            base_temp = 27.0 + 4.0 * np.sin((hour - 8) * np.pi / 12)
        
        temp = float(np.round(base_temp + np.random.normal(0, 1.5), 1))

        # Humidity (%) & Rainfall (mm)
        if month in [6, 7, 8, 9]:  # Monsoon
            humidity = float(np.clip(np.round(75 + np.random.normal(0, 10), 1), 40, 100))
            rainfall = float(np.round(max(0, np.random.exponential(1.5) if np.random.rand() < 0.3 else 0), 1))
        else:
            humidity = float(np.clip(np.round(45 + np.random.normal(0, 8), 1), 20, 90))
            rainfall = float(np.round(max(0, np.random.exponential(0.5) if np.random.rand() < 0.05 else 0), 1))

        # Solar Generation (MU per hour) - peaks 10am to 3pm
        if 6 <= hour <= 18:
            solar_peak = 120.0 * np.sin((hour - 6) * np.pi / 12)
            # Cloud cover effect in monsoon
            cloud_factor = 0.5 if (month in [6, 7, 8, 9] and rainfall > 0) else 1.0
            solar_gen = float(np.round(max(0, solar_peak * cloud_factor + np.random.normal(0, 5)), 2))
        else:
            solar_gen = 0.0

        # Wind Generation (MU per hour) - stronger in monsoon and night
        wind_base = 80.0 if month in [6, 7, 8, 9] else 35.0
        wind_gen = float(np.round(max(0, wind_base + 15.0 * np.cos(hour * np.pi / 12) + np.random.normal(0, 8)), 2))

        # Hydro Generation (MU per hour) - higher in monsoon/post-monsoon
        hydro_base = 90.0 if month in [7, 8, 9, 10] else 50.0
        hydro_gen = float(np.round(max(0, hydro_base + np.random.normal(0, 6)), 2))

        # Holiday & Festival status
        is_holiday_flag = 1 if (date_str in indian_holidays or day_of_week == 6) else 0
        festival_name = indian_holidays.get(date_str, "None")

        # Demand model (Energy Required in MU for the state)
        # Daily dual-peak curve (10-12 AM industrial/commercial, 7-10 PM residential cooling/lighting)
        hourly_pattern = 1.0 + 0.25 * np.sin((hour - 7) * np.pi / 12) + 0.15 * np.sin((hour - 19) * np.pi / 6)
        
        # Temp cooling load effect
        temp_effect = max(0, (temp - 25.0) * 0.04) if temp > 25 else max(0, (18.0 - temp) * 0.02)
        
        # Holiday dip effect (commercial reduction)
        holiday_effect = -0.12 if is_holiday_flag else 0.0

        # Base energy demand (MU)
        base_demand = 350.0 * hourly_pattern * (1.0 + temp_effect + holiday_effect)
        
        # Add random noise
        energy_req = float(np.round(max(100.0, base_demand + np.random.normal(0, 15)), 2))
        energy_avail = float(np.round(energy_req * np.random.uniform(0.97, 1.0), 2))
        peak_demand_mw = float(np.round(energy_req * 18.5 + np.random.normal(0, 50), 1))
        peak_met_mw = float(np.round(min(peak_demand_mw, peak_demand_mw * np.random.uniform(0.96, 1.0)), 1))

        # We take Maharashtra as our primary benchmark dataset row
        records.append({
            "Datetime": ts.strftime("%Y-%m-%d %H:00:00"),
            "State": "Maharashtra",
            "Region": "Western Region",
            "Energy Required (MU)": energy_req,
            "Energy Available (MU)": energy_avail,
            "Peak Demand (MW)": peak_demand_mw,
            "Peak Met (MW)": peak_met_mw,
            "Solar Generation": solar_gen,
            "Wind Generation": wind_gen,
            "Hydro Generation": hydro_gen,
            "Temperature": temp,
            "Rainfall": rainfall,
            "Humidity": humidity,
            "Holiday": is_holiday_flag,
            "Festival": festival_name
        })

    df_out = pd.DataFrame(records)
    
    out_dir = os.path.join(os.path.dirname(__file__), "..", "data", "sample")
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "indian_electricity_sample.csv")
    df_out.to_csv(out_file, index=False)
    print(f"Generated Indian Electricity Sample Dataset with {len(df_out)} rows at: {out_file}")

if __name__ == "__main__":
    generate_indian_electricity_dataset()
