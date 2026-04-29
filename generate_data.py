#!/usr/bin/env python3
"""
Flight Data Generator
=====================

Generates synthetic flight data matching the schema of real airline datasets.
Useful for testing without actual data and understanding expected formats.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_flight_data(n_flights=100000, output_file="flight_data_2024.csv"):
    """
    Generate synthetic flight data for testing.
    
    Args:
        n_flights: Number of synthetic flights to generate
        output_file: Output CSV filename
    """
    
    print(f"[GENERATE] Creating {n_flights:,} synthetic flight records...\n")
    
    # Random seeds for reproducibility
    np.random.seed(42)
    
    # Airline data
    airlines = {
        "9E": "Endeavor Air", "AA": "American Airlines", "AS": "Alaska Airlines",
        "B6": "JetBlue Airways", "DL": "Delta Air Lines", "F9": "Frontier Airlines",
        "G4": "Allegiant Air", "HA": "Hawaiian Airlines", "MQ": "Envoy Air",
        "NK": "Spirit Airlines", "OH": "PSA Airlines", "OO": "SkyWest Airlines",
        "UA": "United Airlines", "WN": "Southwest Airlines", "YX": "Republic Airways"
    }
    
    # Major US airports with cities and states
    airports = {
        "ATL": ("Atlanta", "GA"), "DFW": ("Dallas", "TX"), "DEN": ("Denver", "CO"),
        "ORD": ("Chicago", "IL"), "LAX": ("Los Angeles", "CA"), "JFK": ("New York", "NY"),
        "SFO": ("San Francisco", "CA"), "LAS": ("Las Vegas", "NV"), "SEA": ("Seattle", "WA"),
        "MIA": ("Miami", "FL"), "BOS": ("Boston", "MA"), "LGA": ("New York", "NY"),
        "EWR": ("Newark", "NJ"), "IAH": ("Houston", "TX"), "PHX": ("Phoenix", "AZ"),
        "PHL": ("Philadelphia", "PA"), "CLT": ("Charlotte", "NC"), "DET": ("Detroit", "MI"),
        "MSY": ("New Orleans", "LA"), "SAN": ("San Diego", "CA")
    }
    
    # Realistic delay distributions (mean, std for each airline)
    airline_delay_profile = {
        "AA": (15, 25),  # American - moderate delays
        "DL": (12, 22),  # Delta - better performance
        "UA": (16, 26),  # United - moderate-high delays
        "SW": (10, 20),  # Southwest - better performance
        "B6": (14, 24),  # JetBlue - moderate delays
        "NK": (18, 28),  # Spirit - high delays
        "F9": (17, 27),  # Frontier - high delays
        "AS": (9, 19),   # Alaska - good performance
        "HA": (8, 18),   # Hawaiian - excellent performance
    }
    
    # Seasonal delay variation
    seasonal_multipliers = {
        1: 1.1,   # Jan - winter weather
        2: 1.1,   # Feb - winter weather
        3: 1.0,   # Mar - spring
        4: 0.9,   # Apr - spring (good)
        5: 0.95,  # May - spring
        6: 1.2,   # Jun - summer peak
        7: 1.25,  # Jul - summer peak
        8: 1.2,   # Aug - summer peak
        9: 1.0,   # Sep - fall
        10: 0.95, # Oct - fall (good)
        11: 1.05, # Nov - pre-winter
        12: 1.15  # Dec - holiday peak
    }
    
    # Generate data
    data = {
        'op_unique_carrier': [],
        'origin': [],
        'origin_city_name': [],
        'origin_state_nm': [],
        'dest': [],
        'dest_city_name': [],
        'dest_state_nm': [],
        'dep_delay': [],
        'arr_delay': [],
        'cancelled': [],
        'month': [],
        'distance': []
    }
    
    airline_codes = list(airlines.keys())
    airport_codes = list(airports.keys())
    
    print("[GENERATE] Sampling flight records...")
    
    for i in range(n_flights):
        # Airline selection (weighted by market share)
        carrier = np.random.choice(
            airline_codes,
            p=[0.15, 0.12, 0.08, 0.07, 0.14, 0.06, 0.05, 0.06, 0.06, 0.05, 0.04, 0.05, 0.04, 0.02]
        )
        
        # Origin and destination
        origin = np.random.choice(airport_codes)
        dest = np.random.choice(airport_codes)
        while dest == origin:  # Ensure different airports
            dest = np.random.choice(airport_codes)
        
        # Month (seasonal variation)
        month = np.random.randint(1, 13)
        
        # Distance (realistic US domestic)
        distance = np.random.uniform(300, 2500)
        
        # Cancellation (1-2% rate)
        cancelled = 1 if np.random.random() < 0.015 else 0
        
        # Departure delay with airline + seasonal effects
        airline_key = carrier
        if airline_key in airline_delay_profile:
            mean_delay, std_delay = airline_delay_profile[airline_key]
        else:
            mean_delay, std_delay = 12, 23
        
        seasonal = seasonal_multipliers.get(month, 1.0)
        dep_delay = np.random.normal(mean_delay * seasonal, std_delay)
        
        # Cancelled flights have extreme delays
        if cancelled:
            dep_delay = np.random.uniform(300, 1000)
        else:
            dep_delay = max(dep_delay, -30)  # Minimum early arrival
        
        # Arrival delay (correlated with departure)
        arr_delay = dep_delay + np.random.normal(0, 10)
        if cancelled:
            arr_delay = np.random.uniform(300, 1000)
        else:
            arr_delay = max(arr_delay, -30)
        
        # Populate data
        data['op_unique_carrier'].append(carrier)
        data['origin'].append(origin)
        data['origin_city_name'].append(airports[origin][0])
        data['origin_state_nm'].append(airports[origin][1])
        data['dest'].append(dest)
        data['dest_city_name'].append(airports[dest][0])
        data['dest_state_nm'].append(airports[dest][1])
        data['dep_delay'].append(dep_delay)
        data['arr_delay'].append(arr_delay)
        data['cancelled'].append(cancelled)
        data['month'].append(month)
        data['distance'].append(distance)
        
        # Progress indicator
        if (i + 1) % 10000 == 0:
            print(f"  [{i + 1:,}/{n_flights:,}] records generated...")
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    print(f"\n[GENERATE] Creating DataFrame with {len(df):,} records")
    
    # Save to CSV
    print(f"[SAVE] Writing to {output_file}...")
    df.to_csv(output_file, index=False)
    
    # Statistics
    print(f"\n[STATS] Dataset Statistics:")
    print(f"  Total Records: {len(df):,}")
    print(f"  Unique Airlines: {df['op_unique_carrier'].nunique()}")
    print(f"  Unique Origins: {df['origin'].nunique()}")
    print(f"  Unique Destinations: {df['dest'].nunique()}")
    print(f"  Date Range: Jan-Dec 2024")
    print(f"  Cancelled Flights: {df['cancelled'].sum():,} ({df['cancelled'].mean()*100:.2f}%)")
    print(f"  Avg Departure Delay: {df['dep_delay'].mean():.2f} minutes")
    print(f"  Avg Arrival Delay: {df['arr_delay'].mean():.2f} minutes")
    print(f"  Min Departure Delay: {df['dep_delay'].min():.2f} minutes")
    print(f"  Max Departure Delay: {df['dep_delay'].max():.2f} minutes")
    print(f"  Std Dev Departure Delay: {df['dep_delay'].std():.2f} minutes")
    
    # Verify file
    print(f"\n[VERIFY] File size: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    print(f"[COMPLETE] Data generation successful!\n")
    
    return df

if __name__ == "__main__":
    print("="*60)
    print("  Flight Data Generator for Analytics Engine")
    print("="*60)
    print()
    
    # Generate dataset
    df = generate_flight_data(n_flights=100000, output_file="flight_data_2024.csv")
    
    # Display sample
    print("Sample records:")
    print(df.head(10).to_string(index=False))
    
    print("\n[READY] Data file ready for PySpark analytics engine!")
