#!/usr/bin/env python3
"""
Quick Start Example: Airline Analytics Engine
==============================================

This script demonstrates the complete workflow:
1. Load data
2. Preprocess with PySpark
3. Run distributed analytics
4. Visualize results
"""

from airline_analytics_engine import AirlineAnalyticsEngine
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def print_section(title):
    """Print formatted section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def main():
    # ==================== INITIALIZATION ====================
    print_section("1. INITIALIZING SPARK SESSION")
    
    engine = AirlineAnalyticsEngine(
        app_name="AirlineAnalysis",
        local_mode=True  # Single machine mode
    )
    print("✓ Spark session initialized with optimizations:")
    print("  - Adaptive Query Execution (AQE) enabled")
    print("  - Dynamic partition coalescing enabled")
    print("  - 200 shuffle partitions for wide transformations")
    
    # ==================== DATA LOADING ====================
    print_section("2. LOADING & PREPROCESSING DATA")
    
    # Note: Replace with actual file path
    engine.load_data("flight_data_2024.csv") \
          .preprocess_data()
    
    print("✓ Data loading complete:")
    print(f"  - Total rows loaded: {engine.df.count():,}")
    print(f"  - Columns: {', '.join(engine.df.columns)}")
    print(f"  - Data repartitioned: 8 partitions (Month × Airline)")
    print(f"  - DataFrame cached in memory")
    
    # ==================== STATISTICAL SUMMARY ====================
    print_section("3. STATISTICAL SUMMARY")
    
    summary = engine.statistical_summary()
    summary_pd = summary.toPandas()
    
    for col in summary_pd.columns:
        value = summary_pd[col].iloc[0]
        if col == 'Total_Flights':
            print(f"  {col}: {int(value):,}")
        elif col == 'Cancellation_Rate':
            print(f"  {col}: {value*100:.2f}%")
        else:
            print(f"  {col}: {value:.2f}" if isinstance(value, float) else f"  {col}: {value}")
    
    # ==================== AIRLINE PERFORMANCE ====================
    print_section("4. DISTRIBUTED AIRLINE PERFORMANCE ANALYSIS")
    
    benchmark = engine.airline_performance_benchmark()
    benchmark_pd = benchmark.toPandas()
    
    print("Top 5 Best Performing Airlines (Lowest Delay):")
    print(benchmark_pd.nsmallest(5, 'Avg_Departure_Delay')[
        ['Airline_Name', 'Avg_Departure_Delay', 'Cancellation_Rate']
    ].to_string(index=False))
    
    print("\n\nTop 5 Worst Performing Airlines (Highest Delay):")
    print(benchmark_pd.nlargest(5, 'Avg_Departure_Delay')[
        ['Airline_Name', 'Avg_Departure_Delay', 'Cancellation_Rate']
    ].to_string(index=False))
    
    # Cache for later use
    engine.export_to_cache('benchmark', benchmark)
    
    # ==================== AIRPORT ANALYSIS ====================
    print_section("5. DISTRIBUTED AIRPORT ANALYSIS")
    
    airports = engine.airport_analysis()
    airport_pd = airports.toPandas()
    
    print("Busiest Airports (by flight volume):")
    print(airport_pd.nlargest(5, 'Flight_Count')[
        ['Origin_Airport', 'Origin_City', 'Flight_Count', 'Avg_Departure_Delay']
    ].to_string(index=False))
    
    print("\n\nMost Problematic Airports (highest delay):")
    print(airport_pd.nlargest(5, 'Avg_Departure_Delay')[
        ['Origin_Airport', 'Origin_City', 'Avg_Departure_Delay', 'Flight_Count']
    ].to_string(index=False))
    
    engine.export_to_cache('airports', airports)
    
    # ==================== TEMPORAL ANALYSIS ====================
    print_section("6. TEMPORAL ANALYSIS (SEASONAL PATTERNS)")
    
    temporal = engine.temporal_analysis()
    temporal_pd = temporal.toPandas()
    
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    print("Monthly Average Delays:")
    for _, row in temporal_pd.iterrows():
        month_name = months[int(row['Month'])-1]
        print(f"  {month_name}: {row['Avg_Delay']:.2f} min (σ={row['Delay_StdDev']:.2f})")
    
    engine.export_to_cache('temporal', temporal)
    
    # ==================== BEST TRAVEL MONTHS ====================
    print_section("7. TRAVEL PLANNING ANALYSIS")
    
    best_months = engine.best_travel_months()
    best_months_pd = best_months.toPandas().sort_values('Rank')
    
    print("Best Months to Travel (lowest disruption):")
    for _, row in best_months_pd.head(5).iterrows():
        month_name = months[int(row['Month'])-1]
        print(f"  #{int(row['Rank'])} {month_name}: Score={row['Travel_Score']:.2f} "
              f"(Delay={row['Avg_Delay']:.2f}m, Cancel={row['Cancellation_Rate']*100:.2f}%)")
    
    print("\nWorst Months to Travel (highest disruption):")
    for _, row in best_months_pd.tail(3).iterrows():
        month_name = months[int(row['Month'])-1]
        print(f"  #{int(row['Rank'])} {month_name}: Score={row['Travel_Score']:.2f} "
              f"(Delay={row['Avg_Delay']:.2f}m, Cancel={row['Cancellation_Rate']*100:.2f}%)")
    
    engine.export_to_cache('best_months', best_months)
    
    # ==================== HIGH DELAY ROUTES ====================
    print_section("8. PROBLEMATIC ROUTES (Delay > 60 min)")
    
    high_delay = engine.high_delay_routes(threshold=60)
    high_delay_pd = high_delay.toPandas()
    
    if len(high_delay_pd) > 0:
        print("Top 5 Routes with Most High-Delay Incidents:")
        print(high_delay_pd.head(5)[
            ['Origin_Airport', 'Destination_Airport', 'High_Delay_Count', 'Avg_Delay']
        ].to_string(index=False))
    else:
        print("No routes found with consistent high delays > 60 minutes")
    
    # ==================== WORST PERFORMERS ====================
    print_section("9. COMPREHENSIVE WORST PERFORMER RANKING")
    
    worst = engine.worst_performers(limit=5)
    worst_pd = worst.toPandas()
    
    print("Bottom 5 Airlines (ranked by delay + cancellation):")
    for i, (_, row) in enumerate(worst_pd.iterrows(), 1):
        print(f"  {i}. {row['Airline_Name']}")
        print(f"     Avg Delay: {row['Avg_Departure_Delay']:.2f} min | "
              f"P95 Delay: {row['P95_Departure_Delay']:.2f} min | "
              f"Cancel Rate: {row['Cancellation_Rate']*100:.2f}%")
    
    # ==================== MULTI-DIMENSIONAL ANALYSIS ====================
    print_section("10. AIRLINE-ROUTE ANALYSIS (Sample)")
    
    route_analysis = engine.airline_route_analysis()
    route_pd = route_analysis.toPandas()
    
    if len(route_pd) > 0:
        print("Top 5 Airline-Route Combinations with Highest Delays:")
        print(route_pd.nlargest(5, 'Avg_Delay')[
            ['Airline', 'Origin_Airport', 'Destination_Airport', 'Avg_Delay', 'Flight_Count']
        ].to_string(index=False))
    
    # ==================== VISUALIZATION (Sample) ====================
    print_section("11. GENERATING VISUALIZATIONS")
    
    # Figure 1: Airline comparison
    fig, ax = plt.subplots(figsize=(12, 6))
    top_airlines = benchmark_pd.nlargest(10, 'Avg_Departure_Delay')
    
    ax.barh(range(len(top_airlines)), top_airlines['Avg_Departure_Delay'], 
            color='#dc2626', alpha=0.8, edgecolor='white', linewidth=1)
    ax.set_yticks(range(len(top_airlines)))
    ax.set_yticklabels(top_airlines['Airline_Name'])
    ax.set_xlabel('Average Departure Delay (minutes)')
    ax.set_title('Top 10 Airlines by Average Departure Delay', fontsize=14, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    plt.savefig('airline_delays.png', dpi=150, bbox_inches='tight')
    print("✓ Saved: airline_delays.png")
    
    # Figure 2: Temporal trends
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.plot(range(len(temporal_pd)), temporal_pd['Avg_Delay'], 
            color='#2563eb', linewidth=2.5, marker='o', markersize=6,
            markerfacecolor='white', markeredgewidth=2)
    ax.fill_between(range(len(temporal_pd)), temporal_pd['Avg_Delay'], 
                    alpha=0.1, color='#2563eb')
    ax.set_xticks(range(len(temporal_pd)))
    ax.set_xticklabels(months, fontsize=9)
    ax.set_ylabel('Average Departure Delay (minutes)')
    ax.set_title('Seasonal Delay Trends', fontsize=14, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', alpha=0.2)
    
    plt.tight_layout()
    plt.savefig('seasonal_trends.png', dpi=150, bbox_inches='tight')
    print("✓ Saved: seasonal_trends.png")
    
    # ==================== CACHING STATS ====================
    print_section("12. CACHE STATISTICS")
    
    print(f"Cached DataFrames: {len(engine.cache_store)}")
    for name, df in engine.cache_store.items():
        try:
            row_count = df.count()
            print(f"  - {name}: {row_count:,} rows")
        except:
            print(f"  - {name}: [in-memory cache]")
    
    # ==================== CLEANUP ====================
    print_section("13. CLEANUP & SHUTDOWN")
    
    engine.shutdown()
    print("✓ Spark session terminated")
    print("✓ All cached data released")
    
    # ==================== SUMMARY ====================
    print_section("ANALYSIS COMPLETE")
    
    print("Key Findings:")
    worst_airline = benchmark_pd.nlargest(1, 'Avg_Departure_Delay').iloc[0]
    best_airline = benchmark_pd.nsmallest(1, 'Avg_Departure_Delay').iloc[0]
    best_month = best_months_pd.nsmallest(1, 'Travel_Score').iloc[0]
    
    print(f"  • Worst Airline: {worst_airline['Airline_Name']} "
          f"({worst_airline['Avg_Departure_Delay']:.2f} min avg delay)")
    print(f"  • Best Airline: {best_airline['Airline_Name']} "
          f"({best_airline['Avg_Departure_Delay']:.2f} min avg delay)")
    print(f"  • Best Month to Travel: {months[int(best_month['Month'])-1]} "
          f"(Score={best_month['Travel_Score']:.2f})")
    print(f"  • Total Flights Analyzed: {int(summary_pd['Total_Flights'].iloc[0]):,}")
    
    print("\nNext Steps:")
    print("  1. Run Streamlit dashboard: streamlit run streamlit_dashboard.py")
    print("  2. View generated charts: airline_delays.png, seasonal_trends.png")
    print("  3. Integrate with production data source (S3, HDFS, etc)")
    print("  4. Deploy on Spark cluster for large-scale analytics")

if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError:
        print("\n❌ ERROR: flight_data_2024.csv not found")
        print("   Please ensure the data file is in the current directory")
        print("   Or modify load_data() path in the script")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("   Check that PySpark is installed: pip install pyspark")
