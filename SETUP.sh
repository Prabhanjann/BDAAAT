#!/bin/bash
# ============================================================================
# AIRLINE ANALYTICS: Complete Setup & Execution Guide
# ============================================================================
#
# This script outlines the complete workflow to run the project.
# Execute commands in order as shown below.
#

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║           ✈️  AIRLINE ANALYTICS - COMPLETE SETUP GUIDE            ║"
echo "║                    PySpark Big Data Project                        ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

# ============================================================================
# STEP 1: ENVIRONMENT SETUP
# ============================================================================

echo "📦 STEP 1: ENVIRONMENT SETUP"
echo "─────────────────────────────────────────────────────────────────────"
echo ""
echo "Install required packages:"
echo ""
echo "  pip install pyspark pandas matplotlib seaborn streamlit numpy"
echo ""
echo "Or using conda:"
echo ""
echo "  conda install pyspark pandas matplotlib seaborn streamlit numpy -c conda-forge"
echo ""
echo "Verify installation:"
echo ""
echo "  python -c \"import pyspark; print('PySpark version:', pyspark.__version__)\""
echo "  python -c \"import pandas; print('Pandas version:', pandas.__version__)\""
echo "  python -c \"import streamlit; print('Streamlit version:', streamlit.__version__)\""
echo ""
echo "✓ Expected output: Version numbers confirm successful installation"
echo ""

# ============================================================================
# STEP 2: DATA GENERATION
# ============================================================================

echo "📊 STEP 2: GENERATE SAMPLE DATA"
echo "─────────────────────────────────────────────────────────────────────"
echo ""
echo "Generate 100,000 synthetic flight records:"
echo ""
echo "  python generate_data.py"
echo ""
echo "✓ Output: Creates 'flight_data_2024.csv' (50-100 MB)"
echo ""
echo "Sample output:"
echo "  [GENERATE] Creating 100,000 synthetic flight records..."
echo "  [STATS] Dataset Statistics:"
echo "    Total Records: 100,000"
echo "    Unique Airlines: 15"
echo "    Unique Origins: 20"
echo "    Avg Departure Delay: 11.23 minutes"
echo ""

# ============================================================================
# STEP 3: RUN ANALYTICS ENGINE (OPTIONAL DEMO)
# ============================================================================

echo "🔬 STEP 3: RUN ANALYTICS ENGINE (OPTIONAL)"
echo "─────────────────────────────────────────────────────────────────────"
echo ""
echo "Execute complete analytics pipeline with example outputs:"
echo ""
echo "  python quick_start.py"
echo ""
echo "✓ Output: Complete analysis with results and visualizations"
echo ""
echo "What this does:"
echo "  1. Initializes PySpark session with optimizations"
echo "  2. Loads flight_data_2024.csv (100K rows)"
echo "  3. Preprocesses & partitions data strategically"
echo "  4. Runs distributed analytics:"
echo "     - Airline performance benchmarking"
echo "     - Airport analysis (busiest, most problematic)"
echo "     - Temporal trends (seasonal patterns)"
echo "     - Route analysis (high-delay routes)"
echo "     - Travel planning (best/worst months)"
echo "  5. Generates matplotlib visualizations:"
echo "     - airline_delays.png"
echo "     - seasonal_trends.png"
echo "  6. Caches results for dashboard"
echo ""
echo "Expected runtime: 30-60 seconds"
echo ""

# ============================================================================
# STEP 4: LAUNCH STREAMLIT DASHBOARD
# ============================================================================

echo "🎨 STEP 4: LAUNCH INTERACTIVE DASHBOARD"
echo "─────────────────────────────────────────────────────────────────────"
echo ""
echo "Start Streamlit server:"
echo ""
echo "  streamlit run streamlit_dashboard.py"
echo ""
echo "✓ Output:"
echo "  You can now view your Streamlit app in your browser."
echo "  Local URL: http://localhost:8501"
echo ""
echo "Dashboard Features:"
echo "  ✈️  Key Metrics (4 cards: flights, delays, cancellation, best airline)"
echo "  📊 Airline Performance (worst performers, delay distribution)"
echo "  📍 Airport Analysis (busiest, most problematic)"
echo "  📅 Travel Planning (best months, quality scoring)"
echo "  📈 Trend Analysis (seasonal delays, monthly breakdown)"
echo ""
echo "Design:"
echo "  • Minimal aesthetic (clean, data-first)"
echo "  • Matplotlib-generated charts"
echo "  • Responsive layout"
echo "  • Color-coded insights"
echo ""
echo "To stop: Press Ctrl+C in terminal"
echo ""

# ============================================================================
# STEP 5: EXPLORATION & CUSTOMIZATION
# ============================================================================

echo "🔧 STEP 5: CUSTOMIZE & EXPLORE"
echo "─────────────────────────────────────────────────────────────────────"
echo ""
echo "Modify analytics engine for custom queries:"
echo ""
echo "  # Edit: airline_analytics_engine.py"
echo "  # Add new analysis methods following existing patterns"
echo ""
echo "Create custom Jupyter notebook:"
echo ""
echo "  from airline_analytics_engine import AirlineAnalyticsEngine"
echo "  engine = AirlineAnalyticsEngine()"
echo "  engine.load_data('flight_data_2024.csv').preprocess_data()"
echo "  benchmark = engine.airline_performance_benchmark()"
echo "  print(benchmark.show(10))"
echo ""
echo "Export results to other formats:"
echo ""
echo "  # Get as Pandas DataFrame"
echo "  df_pandas = benchmark.toPandas()"
echo "  df_pandas.to_csv('results.csv', index=False)"
echo "  df_pandas.to_json('results.json')"
echo ""

# ============================================================================
# STEP 6: PRODUCTION DEPLOYMENT
# ============================================================================

echo "🚀 STEP 6: DEPLOY TO PRODUCTION (ADVANCED)"
echo "─────────────────────────────────────────────────────────────────────"
echo ""
echo "For real datasets on distributed cluster:"
echo ""
echo "1. Prepare data in Parquet format (columnar, compressed):"
echo ""
echo "   spark-submit \\"
echo "     --master spark://cluster-master:7077 \\"
echo "     --num-executors 10 \\"
echo "     --executor-cores 4 \\"
echo "     --executor-memory 16G \\"
echo "     process_raw_data.py"
echo ""
echo "2. Deploy Streamlit on server:"
echo ""
echo "   streamlit run streamlit_dashboard.py \\"
echo "     --server.port 80 \\"
echo "     --logger.level=error"
echo ""
echo "3. Set up monitoring:"
echo "   - Spark Web UI: http://cluster-master:4040"
echo "   - Resource Manager: http://cluster-master:8088"
echo "   - Streamlit Metrics: Custom dashboard"
echo ""

# ============================================================================
# PROJECT STRUCTURE
# ============================================================================

echo "📁 PROJECT STRUCTURE"
echo "─────────────────────────────────────────────────────────────────────"
echo ""
echo "airline-analytics/"
echo "│"
echo "├── airline_analytics_engine.py (600+ lines)"
echo "│   • Core PySpark analytics engine"
echo "│   • 10 major analysis methods"
echo "│   • BDA optimization patterns"
echo "│"
echo "├── streamlit_dashboard.py (400+ lines)"
echo "│   • Interactive visualization interface"
echo "│   • Minimal aesthetic design"
echo "│   • 5+ chart types with matplotlib"
echo "│"
echo "├── quick_start.py (300+ lines)"
echo "│   • Complete usage example"
echo "│   • Demonstrates all features"
echo "│   • Chart generation & exports"
echo "│"
echo "├── generate_data.py"
echo "│   • Synthetic flight data generator"
echo "│   • 100K realistic records"
echo "│   • Configurable parameters"
echo "│"
echo "├── BDA_GUIDE.md (1000+ words)"
echo "│   • 10 BDA concepts explained"
echo "│   • Code examples & rationale"
echo "│   • Performance considerations"
echo "│"
echo "├── README.md"
echo "│   • Project overview"
echo "│   • Architecture & design"
echo "│   • Educational value"
echo "│"
echo "└── flight_data_2024.csv"
echo "    • Sample dataset (generated)"
echo "    • 100K records, 13 columns"
echo ""

# ============================================================================
# QUICK REFERENCE
# ============================================================================

echo "⚡ QUICK REFERENCE"
echo "─────────────────────────────────────────────────────────────────────"
echo ""
echo "Generate data:"
echo "  python generate_data.py"
echo ""
echo "Run example analysis:"
echo "  python quick_start.py"
echo ""
echo "Launch dashboard:"
echo "  streamlit run streamlit_dashboard.py"
echo ""
echo "Check Spark version:"
echo "  python -c \"import pyspark; print(pyspark.__version__)\""
echo ""
echo "Clean up:"
echo "  rm -f *.pyc __pycache__ *.csv airline_delays.png seasonal_trends.png"
echo ""

# ============================================================================
# TROUBLESHOOTING
# ============================================================================

echo "🔧 TROUBLESHOOTING"
echo "─────────────────────────────────────────────────────────────────────"
echo ""
echo "Issue: PySpark not found"
echo "  Solution: pip install pyspark --upgrade"
echo ""
echo "Issue: Java not found"
echo "  Solution: install-jdk (requires Java 8+)"
echo ""
echo "Issue: Out of memory"
echo "  Solution: Reduce data size or run quick_start.py with smaller n_flights"
echo ""
echo "Issue: Streamlit port already in use"
echo "  Solution: streamlit run streamlit_dashboard.py --server.port 8502"
echo ""
echo "Issue: CSV file not found"
echo "  Solution: Run 'python generate_data.py' first"
echo ""

# ============================================================================
# NEXT STEPS
# ============================================================================

echo "📚 NEXT STEPS FOR LEARNING"
echo "─────────────────────────────────────────────────────────────────────"
echo ""
echo "1. Read BDA_GUIDE.md to understand 10 key concepts"
echo ""
echo "2. Study airline_analytics_engine.py:"
echo "   - Partitioning strategies (line 50)"
echo "   - Caching patterns (line 70)"
echo "   - Window functions (line 150)"
echo "   - Aggregations (line 100)"
echo ""
echo "3. Modify quick_start.py:"
echo "   - Change delay threshold: threshold=45"
echo "   - Add new metrics"
echo "   - Export to different formats"
echo ""
echo "4. Customize dashboard:"
echo "   - Add new tabs"
echo "   - Create custom charts"
echo "   - Integrate with live data"
echo ""
echo "5. Explore PySpark docs:"
echo "   - https://spark.apache.org/docs/latest/sql-programming-guide.html"
echo ""

# ============================================================================
# VERIFICATION CHECKLIST
# ============================================================================

echo "✅ VERIFICATION CHECKLIST"
echo "─────────────────────────────────────────────────────────────────────"
echo ""
echo "After setup, verify:"
echo ""
echo "  ☐ Python 3.7+ installed:      python --version"
echo "  ☐ PySpark installed:          pip show pyspark"
echo "  ☐ Java 8+ installed:          java -version"
echo "  ☐ Dependencies installed:     pip list | grep streamlit"
echo "  ☐ Data generated:             ls -lh flight_data_2024.csv"
echo "  ☐ Quick start runs:           python quick_start.py"
echo "  ☐ Dashboard launches:         streamlit run streamlit_dashboard.py"
echo ""
echo "All checks passed? You're ready! 🚀"
echo ""

# ============================================================================
# SUMMARY
# ============================================================================

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                      SETUP COMPLETE ✓                             ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""
echo "Your airline analytics system is ready!"
echo ""
echo "Quick start (3 commands):"
echo ""
echo "  1. python generate_data.py"
echo "  2. python quick_start.py                  (optional)"
echo "  3. streamlit run streamlit_dashboard.py"
echo ""
echo "Then open: http://localhost:8501"
echo ""
echo "Happy analyzing! ✈️📊"
echo ""
