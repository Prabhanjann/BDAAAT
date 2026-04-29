    from pyspark.sql import SparkSession

    spark = SparkSession.builder \
        .appName("AirlineAnalysis") \
        .getOrCreate()

    from pyspark.sql.functions import avg, count, col, desc, when

    df = spark.read.csv("flight_data_2024.csv", header=True, inferSchema=True)

    # Select + rename columns (VERY IMPORTANT)
    df = df.select(
        col("op_unique_carrier").alias("Airline"),
        col("origin").alias("Origin_Airport"),
        col("origin_city_name").alias("Origin_City"),
        col("origin_state_nm").alias("Origin_State"),
        col("dest").alias("Destination_Airport"),
        col("dest_city_name").alias("Destination_City"),
        col("dest_state_nm").alias("Destination_State"),
        col("dep_delay").alias("Departure_Delay"),
        col("arr_delay").alias("Arrival_Delay"),
        col("cancelled").alias("Cancelled"),
        col("month").alias("Month")
    )

    df = df.dropna()

    # Airline code to airline name mapping
    df = df.withColumn(
        "Airline_Name",
        when(col("Airline") == "9E", "Endeavor Air")
        .when(col("Airline") == "AA", "American Airlines")
        .when(col("Airline") == "AS", "Alaska Airlines")
        .when(col("Airline") == "B6", "JetBlue Airways")
        .when(col("Airline") == "DL", "Delta Air Lines")
        .when(col("Airline") == "F9", "Frontier Airlines")
        .when(col("Airline") == "G4", "Allegiant Air")
        .when(col("Airline") == "HA", "Hawaiian Airlines")
        .when(col("Airline") == "MQ", "Envoy Air")
        .when(col("Airline") == "NK", "Spirit Airlines")
        .when(col("Airline") == "OH", "PSA Airlines")
        .when(col("Airline") == "OO", "SkyWest Airlines")
        .when(col("Airline") == "UA", "United Airlines")
        .when(col("Airline") == "WN", "Southwest Airlines")
        .when(col("Airline") == "YX", "Republic Airways")
        .otherwise("Unknown Carrier")
    )

    #Average departure delay by airline

    avg_delay = df.groupBy("Airline", "Airline_Name") \
        .agg(avg("Departure_Delay").alias("Avg_Departure_Delay")) \
        .orderBy("Avg_Departure_Delay")

    avg_delay.show(truncate=False)

    # Cancellation rate by airline

    cancel_rate = df.groupBy("Airline", "Airline_Name") \
        .agg(avg("Cancelled").alias("Cancellation_Rate")) \
        .orderBy("Cancellation_Rate", ascending=False)

    cancel_rate.show(truncate=False)

    # Average departure delay by origin airport

    delay_airports = df.groupBy("Origin_Airport", "Origin_City", "Origin_State") \
        .agg(avg("Departure_Delay").alias("Avg_Delay")) \
        .orderBy("Avg_Delay", ascending=False)

    delay_airports.show(truncate=False)

    # Most common origin airports (by number of flights) --> Busiest airports

    busy_airports = df.groupBy("Origin_Airport", "Origin_City", "Origin_State") \
        .agg(count("*").alias("Flight_Count")) \
        .orderBy("Flight_Count", ascending=False)

    busy_airports.show(truncate=False)

    # Average departure delay by month

    month_delay = df.groupBy("Month") \
        .agg(avg("Departure_Delay").alias("Avg_Delay")) \
        .orderBy("Month")

    month_delay.show()

    # Combine average departure delay and cancellation rate for a comprehensive airline performance benchmark --> Benchmarking airlines based on both delay and cancellation metrics

    benchmark = avg_delay.join(cancel_rate, ["Airline", "Airline_Name"])
    benchmark.show(truncate=False)
        
    # Count of flights with high departure delay (> 60 minutes) by airline

    high_delay = df.filter(col("Departure_Delay") > 60)

    high_delay.groupBy("Airline", "Airline_Name") \
        .count() \
        .orderBy("count", ascending=False) \
        .show(truncate=False)

    # Worst performing airlines (average departure delay and cancellation rate) --> Airlines with the highest average departure delay and cancellation rate are considered the worst performers

    worst = benchmark.orderBy(desc("Avg_Departure_Delay"), desc("Cancellation_Rate"))
    worst.show(truncate=False)
        
        
    spark.stop()