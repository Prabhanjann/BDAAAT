"""
PySpark Distributed Airline Analytics Engine
==============================================
Big Data Analytics Project: Flight Performance Benchmarking
Demonstrates key BDA concepts: distributed computing, data partitioning, 
query optimization, and scalable analytics workflows.
"""

from pyspark.sql import SparkSession, Window
from pyspark.sql.functions import (
    avg, count, col, desc, when, round, month, year, 
    percentile_approx, stddev_pop, max as spark_max, min as spark_min,
    collect_list, struct, row_number, dense_rank
)
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType
import pickle
import os

class AirlineAnalyticsEngine:
    """
    Distributed analytics engine for airline performance analysis.
    Implements BDA best practices: lazy evaluation, partitioning, caching, and query optimization.
    """
    
    def __init__(self, app_name="AirlineAnalysis", local_mode=True):
        """
        Initialize Spark session with optimized configurations.
        
        Args:
            app_name: Name of the Spark application
            local_mode: If True, runs in local[*] mode for development
        """
        self.spark = SparkSession.builder \
            .appName(app_name) \
            .config("spark.sql.adaptive.enabled", "true") \
            .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
            .config("spark.sql.shuffle.partitions", "200") \
            .config("spark.default.parallelism", "8") \
            .master("local[*]" if local_mode else None) \
            .getOrCreate()
        
        # Set log level
        self.spark.sparkContext.setLogLevel("WARN")
        self.df = None
        self.cache_store = {}
    
    def load_data(self, file_path):
        """
        Load flight data with schema inference.
        Demonstrates: lazy loading, schema inference
        
        Args:
            file_path: Path to CSV file
        """
        print(f"[LOAD] Reading data from {file_path}...")
        self.df = self.spark.read.csv(
            file_path,
            header=True,
            inferSchema=True,
            samplingRatio=0.1  # BDA optimization: sample for schema inference
        )
        
        print(f"[LOAD] Data shape: {self.df.count()} rows")
        print(f"[LOAD] Columns: {len(self.df.columns)}")
        return self
    
    def preprocess_data(self):
        """
        Clean and transform raw data.
        Demonstrates: column selection, data type conversion, null handling
        """
        print("[PREPROCESS] Starting data transformation...")
        
        # Select and rename columns (explicit schema projection)
        self.df = self.df.select(
            col("op_unique_carrier").alias("Airline"),
            col("origin").alias("Origin_Airport"),
            col("origin_city_name").alias("Origin_City"),
            col("origin_state_nm").alias("Origin_State"),
            col("dest").alias("Destination_Airport"),
            col("dest_city_name").alias("Destination_City"),
            col("dest_state_nm").alias("Destination_State"),
            col("dep_delay").cast(DoubleType()).alias("Departure_Delay"),
            col("arr_delay").cast(DoubleType()).alias("Arrival_Delay"),
            col("cancelled").cast(IntegerType()).alias("Cancelled"),
            col("month").cast(IntegerType()).alias("Month"),
            col("distance").cast(DoubleType()).alias("Distance")
        )
        
        # Handle missing values strategically
        self.df = self.df.dropna(subset=["Departure_Delay", "Arrival_Delay", "Cancelled"])
        
        # Create airline mapping using UDF approach for scalability
        airline_mapping = {
            "9E": "Endeavor Air", "AA": "American Airlines", "AS": "Alaska Airlines",
            "B6": "JetBlue Airways", "DL": "Delta Air Lines", "F9": "Frontier Airlines",
            "G4": "Allegiant Air", "HA": "Hawaiian Airlines", "MQ": "Envoy Air",
            "NK": "Spirit Airlines", "OH": "PSA Airlines", "OO": "SkyWest Airlines",
            "UA": "United Airlines", "WN": "Southwest Airlines", "YX": "Republic Airways"
        }
        
        # Use when/otherwise for mapping (more efficient than Python UDF)
        mapping_expr = when(col("Airline") == "9E", "Endeavor Air")
        for code, name in list(airline_mapping.items())[1:]:
            mapping_expr = mapping_expr.when(col("Airline") == code, name)
        mapping_expr = mapping_expr.otherwise("Unknown Carrier")
        
        self.df = self.df.withColumn("Airline_Name", mapping_expr)
        
        # Partition data strategically for optimization
        # Demonstrates: data partitioning for distributed processing
        self.df = self.df.repartition(
            8,  # Number of partitions
            col("Month"),  # Partition by month for temporal locality
            col("Airline")  # And airline for access patterns
        )
        
        # Cache the preprocessed dataframe (BDA optimization)
        self.df.cache()
        self.df.count()  # Force evaluation
        
        print("[PREPROCESS] Data preprocessed and cached")
        return self
    
    # ==================== DISTRIBUTED ANALYTICS METHODS ====================
    
    def airline_performance_benchmark(self):
        """
        Comprehensive airline performance metrics.
        Demonstrates: aggregation, window functions, multiple metrics
        """
        print("[COMPUTE] Calculating airline performance metrics...")
        
        benchmark = self.df.groupBy("Airline", "Airline_Name") \
            .agg(
                count("*").alias("Total_Flights"),
                round(avg("Departure_Delay"), 2).alias("Avg_Departure_Delay"),
                round(avg("Arrival_Delay"), 2).alias("Avg_Arrival_Delay"),
                round(percentile_approx("Departure_Delay", 0.75), 2).alias("P75_Departure_Delay"),
                round(percentile_approx("Departure_Delay", 0.95), 2).alias("P95_Departure_Delay"),
                round(avg("Cancelled"), 4).alias("Cancellation_Rate"),
                round(stddev_pop("Departure_Delay"), 2).alias("Delay_StdDev")
            ) \
            .orderBy(desc("Avg_Departure_Delay"))
        
        benchmark.cache()
        self.cache_store['airline_benchmark'] = benchmark
        return benchmark
    
    def airport_analysis(self):
        """
        Distributed analysis of airport performance.
        Demonstrates: groupBy with multiple dimensions, aggregations at scale
        """
        print("[COMPUTE] Analyzing airport performance...")
        
        # Origin airport analysis
        origin_analysis = self.df.groupBy(
            "Origin_Airport", 
            "Origin_City", 
            "Origin_State"
        ).agg(
            count("*").alias("Flight_Count"),
            round(avg("Departure_Delay"), 2).alias("Avg_Departure_Delay"),
            round(percentile_approx("Departure_Delay", 0.90), 2).alias("P90_Delay"),
            round(avg("Cancelled"), 4).alias("Cancellation_Rate")
        ).filter(col("Flight_Count") >= 50)  # Filter for statistical significance
        
        origin_analysis.cache()
        self.cache_store['airport_analysis'] = origin_analysis
        
        return origin_analysis
    
    def temporal_analysis(self):
        """
        Time-series analysis by month.
        Demonstrates: temporal aggregation, trend analysis
        """
        print("[COMPUTE] Computing temporal trends...")
        
        temporal = self.df.groupBy("Month") \
            .agg(
                count("*").alias("Total_Flights"),
                round(avg("Departure_Delay"), 2).alias("Avg_Delay"),
                round(avg("Arrival_Delay"), 2).alias("Avg_Arrival_Delay"),
                round(percentile_approx("Departure_Delay", 0.75), 2).alias("P75_Delay"),
                round(avg("Cancelled"), 4).alias("Cancellation_Rate"),
                round(stddev_pop("Departure_Delay"), 2).alias("Delay_StdDev")
            ).orderBy("Month")
        
        temporal.cache()
        self.cache_store['temporal_analysis'] = temporal
        
        return temporal
    
    def high_delay_routes(self, threshold=60):
        """
        Identify problematic routes with high delays.
        Demonstrates: filtering, multi-dimensional grouping, percentile analysis
        """
        print(f"[COMPUTE] Finding routes with departure delay > {threshold} min...")
        
        high_delay = self.df.filter(col("Departure_Delay") > threshold) \
            .groupBy("Origin_Airport", "Destination_Airport") \
            .agg(
                count("*").alias("High_Delay_Count"),
                round(avg("Departure_Delay"), 2).alias("Avg_Delay"),
                round(avg("Distance"), 0).alias("Distance_Miles")
            ).filter(col("High_Delay_Count") >= 5) \
            .orderBy(desc("High_Delay_Count"))
        
        high_delay.cache()
        return high_delay
    
    def airline_route_analysis(self):
        """
        Multi-dimensional analysis: airline + route combinations.
        Demonstrates: complex grouping, window functions
        """
        print("[COMPUTE] Analyzing airline-route combinations...")
        
        route_perf = self.df.groupBy(
            "Airline", 
            "Airline_Name",
            "Origin_Airport",
            "Destination_Airport"
        ).agg(
            count("*").alias("Flight_Count"),
            round(avg("Departure_Delay"), 2).alias("Avg_Delay"),
            round(avg("Distance"), 0).alias("Distance")
        ).filter(col("Flight_Count") >= 10) \
         .orderBy("Airline", desc("Avg_Delay"))
        
        route_perf.cache()
        return route_perf
    
    def worst_performers(self, limit=10):
        """
        Identify worst performing airlines.
        Demonstrates: sorting, ranking, multi-metric optimization
        """
        print("[COMPUTE] Identifying worst performers...")
        
        benchmark = self.airline_performance_benchmark()
        worst = benchmark.orderBy(
            desc("Avg_Departure_Delay"),
            desc("Cancellation_Rate")
        ).limit(limit)
        
        return worst
    
    def best_travel_months(self):
        """
        Determine optimal months for travel.
        Demonstrates: ranking, window functions
        """
        print("[COMPUTE] Ranking months for travel quality...")
        
        temporal = self.temporal_analysis()
        
        # Rank months by combined delay + cancellation score
        ranked = temporal.withColumn(
            "Travel_Score",
            round(
                (col("Avg_Delay") * 0.7 + col("Cancellation_Rate") * 100 * 0.3), 
                2
            )
        ).withColumn(
            "Rank",
            dense_rank().over(Window.orderBy("Travel_Score"))
        ).select(
            "Month", "Travel_Score", "Rank", "Avg_Delay", 
            "Cancellation_Rate", "Delay_StdDev"
        )
        
        ranked.cache()
        return ranked
    
    def statistical_summary(self):
        """
        Overall statistical summary using RDD-level operations.
        Demonstrates: distributed statistics, quantile computation
        """
        print("[COMPUTE] Computing statistical summary...")
        
        summary = self.df.agg(
            count("*").alias("Total_Flights"),
            avg("Departure_Delay").alias("Avg_Departure_Delay"),
            spark_min("Departure_Delay").alias("Min_Delay"),
            spark_max("Departure_Delay").alias("Max_Delay"),
            percentile_approx("Departure_Delay", 0.5).alias("Median_Delay"),
            percentile_approx("Departure_Delay", 0.95).alias("P95_Delay"),
            stddev_pop("Departure_Delay").alias("StdDev"),
            avg("Cancelled").alias("Cancellation_Rate"),
            round(avg("Distance"), 2).alias("Avg_Distance")
        )
        
        return summary
    
    # ==================== DATA EXPORT METHODS ====================
    
    def export_to_cache(self, name, dataframe):
        """Cache computation results for frontend access"""
        self.cache_store[name] = dataframe
        return dataframe
    
    def get_cached_data(self, name):
        """Retrieve cached results"""
        return self.cache_store.get(name)
    
    def to_pandas_cached(self, name, limit=10000):
        """Convert Spark DataFrame to Pandas for Streamlit (with limit)"""
        df = self.cache_store.get(name)
        if df is None:
            return None
        return df.limit(limit).toPandas()
    
    def shutdown(self):
        """Cleanup resources"""
        self.spark.stop()
        print("[SHUTDOWN] Spark session closed")


# ==================== USAGE EXAMPLE ====================
if __name__ == "__main__":
    # Initialize engine
    engine = AirlineAnalyticsEngine(app_name="AirlineAnalysis", local_mode=True)
    
    # Load and process data
    engine.load_data("flight_data_2024.csv") \
          .preprocess_data()
    
    # Run analyses
    benchmark = engine.airline_performance_benchmark()
    airports = engine.airport_analysis()
    temporal = engine.temporal_analysis()
    worst = engine.worst_performers()
    best_months = engine.best_travel_months()
    summary = engine.statistical_summary()
    
    print("\n[RESULTS] Sample airline benchmark:")
    benchmark.show(5, truncate=False)
    
    print("\n[RESULTS] Best months to travel:")
    best_months.show(5, truncate=False)
    
    engine.shutdown()
