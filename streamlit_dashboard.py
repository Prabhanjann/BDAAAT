"""
Airline Analytics Dashboard
============================
Minimalist Streamlit interface for distributed airline performance analysis.
Clean, data-first aesthetic with focus on insights.
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Configure Streamlit page
st.set_page_config(
    page_title="Flight Analytics",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Minimal, clean CSS styling
st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
    }
    
    body {
        background-color: #fafaf9;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        color: #1f2937;
    }
    
    .main {
        padding: 2rem 3rem;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    header {
        border-bottom: 1px solid #e5e7eb;
        padding-bottom: 2rem;
        margin-bottom: 3rem;
    }
    
    h1 {
        font-size: 2.5rem;
        font-weight: 300;
        letter-spacing: -0.02em;
        margin-bottom: 0.5rem;
        color: #000;
    }
    
    .subtitle {
        font-size: 0.95rem;
        color: #6b7280;
        font-weight: 400;
        letter-spacing: 0.01em;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border: 1px solid #e5e7eb;
        border-radius: 6px;
        transition: all 0.2s ease;
    }
    
    .metric-card:hover {
        border-color: #d1d5db;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    .metric-value {
        font-size: 1.875rem;
        font-weight: 600;
        color: #1f2937;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.875rem;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 500;
    }
    
    .section-title {
        font-size: 1.5rem;
        font-weight: 500;
        margin-top: 2.5rem;
        margin-bottom: 1.5rem;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid #000;
        color: #1f2937;
    }
    
    .chart-container {
        background: white;
        padding: 1.5rem;
        border: 1px solid #e5e7eb;
        border-radius: 6px;
        margin-bottom: 1.5rem;
    }
    
    .data-table {
        font-size: 0.9rem;
        line-height: 1.6;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 1.875rem;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        border-bottom: 1px solid #e5e7eb;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 1rem 1.5rem;
        border-bottom: 2px solid transparent;
        color: #6b7280;
        font-size: 0.9rem;
    }
    
    .stTabs [aria-selected="true"] {
        border-bottom-color: #000;
        color: #1f2937;
    }
</style>
""", unsafe_allow_html=True)

# ==================== HELPER FUNCTIONS ====================

def get_color_palette():
    """Minimal color palette for charts"""
    return {
        'primary': '#1f2937',
        'secondary': '#6b7280',
        'accent': '#2563eb',
        'accent_light': '#dbeafe',
        'danger': '#dc2626',
        'success': '#059669',
        'neutral': '#f3f4f6'
    }

def create_figure(title="", figsize=(12, 6)):
    """Create minimalist matplotlib figure"""
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor('#fafaf9')
    ax.set_facecolor('white')
    
    # Minimal spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#e5e7eb')
    ax.spines['bottom'].set_color('#e5e7eb')
    
    ax.grid(axis='y', alpha=0.1, linestyle='-', linewidth=0.5, color='#e5e7eb')
    
    return fig, ax

def plot_airline_performance(benchmark_df):
    """Airline performance comparison chart"""
    top_airlines = benchmark_df.nlargest(10, 'Avg_Departure_Delay')
    
    fig, ax = create_figure(figsize=(13, 7))
    
    colors = get_color_palette()
    bars = ax.barh(
        range(len(top_airlines)),
        top_airlines['Avg_Departure_Delay'].values,
        color=colors['danger'],
        alpha=0.85,
        edgecolor='white',
        linewidth=1
    )
    
    ax.set_yticks(range(len(top_airlines)))
    ax.set_yticklabels(top_airlines['Airline_Name'].values, fontsize=10)
    ax.set_xlabel('Average Departure Delay (minutes)', fontsize=11, color=colors['secondary'])
    ax.set_title('Worst Performing Airlines', fontsize=13, fontweight=600, pad=20, loc='left')
    
    # Add value labels
    for i, (idx, row) in enumerate(top_airlines.iterrows()):
        ax.text(row['Avg_Departure_Delay'] + 0.3, i, f"{row['Avg_Departure_Delay']:.1f}m", 
                va='center', fontsize=9, color=colors['primary'])
    
    plt.tight_layout()
    return fig

def plot_best_travel_months(best_months_df):
    """Optimal travel months visualization"""
    fig, ax = create_figure(figsize=(13, 6))
    
    colors = get_color_palette()
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    # Sort by month
    data = best_months_df.sort_values('Month').copy()
    month_labels = [months[int(m)-1] for m in data['Month']]
    
    # Create bars with gradient color
    travel_scores = data['Travel_Score'].values
    normalized_scores = (travel_scores - travel_scores.min()) / (travel_scores.max() - travel_scores.min())
    
    bar_colors = [plt.cm.RdYlGn_r(score) for score in normalized_scores]
    
    bars = ax.bar(
        range(len(data)),
        travel_scores,
        color=bar_colors,
        alpha=0.85,
        edgecolor='white',
        linewidth=1
    )
    
    ax.set_xticks(range(len(data)))
    ax.set_xticklabels(month_labels, fontsize=10)
    ax.set_ylabel('Travel Score (Lower is Better)', fontsize=11, color=colors['secondary'])
    ax.set_title('Best Months to Travel', fontsize=13, fontweight=600, pad=20, loc='left')
    
    # Add value labels
    for i, (idx, row) in enumerate(data.iterrows()):
        ax.text(i, row['Travel_Score'] + 0.5, f"{row['Travel_Score']:.1f}", 
                ha='center', va='bottom', fontsize=8, color=colors['primary'])
    
    # Add legend for interpretation
    good = mpatches.Patch(color=plt.cm.RdYlGn_r(0), alpha=0.85, label='Best')
    mid = mpatches.Patch(color=plt.cm.RdYlGn_r(0.5), alpha=0.85, label='Moderate')
    bad = mpatches.Patch(color=plt.cm.RdYlGn_r(1), alpha=0.85, label='Avoid')
    ax.legend(handles=[good, mid, bad], loc='upper left', frameon=False, fontsize=9)
    
    plt.tight_layout()
    return fig

def plot_airport_heatmap(airport_df):
    """Top airports by volume and delay"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.patch.set_facecolor('#fafaf9')
    
    colors = get_color_palette()
    
    # Top airports by volume
    top_airports = airport_df.nlargest(8, 'Flight_Count')
    
    for ax in [ax1, ax2]:
        ax.set_facecolor('white')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#e5e7eb')
        ax.spines['bottom'].set_color('#e5e7eb')
        ax.grid(axis='y', alpha=0.1, linestyle='-', linewidth=0.5, color='#e5e7eb')
    
    # Chart 1: Busiest airports
    bars1 = ax1.barh(
        range(len(top_airports)),
        top_airports['Flight_Count'].values,
        color=colors['accent'],
        alpha=0.85,
        edgecolor='white',
        linewidth=1
    )
    ax1.set_yticks(range(len(top_airports)))
    ax1.set_yticklabels([f"{row['Origin_Airport']} ({row['Origin_City']})" 
                          for _, row in top_airports.iterrows()], fontsize=9)
    ax1.set_xlabel('Number of Flights', fontsize=11, color=colors['secondary'])
    ax1.set_title('Busiest Airports', fontsize=12, fontweight=600, pad=15, loc='left')
    
    # Chart 2: Most problematic airports
    worst_airports = airport_df.nlargest(8, 'Avg_Departure_Delay')
    bars2 = ax2.barh(
        range(len(worst_airports)),
        worst_airports['Avg_Departure_Delay'].values,
        color=colors['danger'],
        alpha=0.85,
        edgecolor='white',
        linewidth=1
    )
    ax2.set_yticks(range(len(worst_airports)))
    ax2.set_yticklabels([f"{row['Origin_Airport']} ({row['Origin_City']})" 
                          for _, row in worst_airports.iterrows()], fontsize=9)
    ax2.set_xlabel('Avg Departure Delay (min)', fontsize=11, color=colors['secondary'])
    ax2.set_title('Most Problematic Airports', fontsize=12, fontweight=600, pad=15, loc='left')
    
    plt.tight_layout()
    return fig

def plot_delay_distribution(benchmark_df):
    """Distribution of delays with statistical markers"""
    fig, ax = create_figure(figsize=(13, 6))
    
    colors = get_color_palette()
    
    # Create scatter plot
    airlines = benchmark_df.sort_values('Avg_Departure_Delay', ascending=False).head(15)
    
    scatter = ax.scatter(
        airlines['Avg_Departure_Delay'],
        airlines['P95_Departure_Delay'],
        s=airlines['Total_Flights']/5,
        alpha=0.6,
        color=colors['accent'],
        edgecolors='white',
        linewidth=1.5
    )
    
    # Add labels
    for idx, row in airlines.iterrows():
        ax.annotate(
            row['Airline'],
            (row['Avg_Departure_Delay'], row['P95_Departure_Delay']),
            fontsize=8,
            alpha=0.7
        )
    
    ax.set_xlabel('Average Departure Delay (min)', fontsize=11, color=colors['secondary'])
    ax.set_ylabel('95th Percentile Delay (min)', fontsize=11, color=colors['secondary'])
    ax.set_title('Delay Characteristics by Airline', fontsize=13, fontweight=600, pad=20, loc='left')
    
    # Add diagonal reference line
    max_val = max(airlines['Avg_Departure_Delay'].max(), airlines['P95_Departure_Delay'].max())
    ax.plot([0, max_val], [0, max_val], 'k--', alpha=0.1, linewidth=1)
    
    plt.tight_layout()
    return fig

def plot_temporal_trends(temporal_df):
    """Monthly trends in delays and cancellations"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(13, 8))
    fig.patch.set_facecolor('#fafaf9')
    
    colors = get_color_palette()
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    month_labels = [months[int(m)-1] for m in temporal_df['Month']]
    
    for ax in [ax1, ax2]:
        ax.set_facecolor('white')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#e5e7eb')
        ax.spines['bottom'].set_color('#e5e7eb')
        ax.grid(axis='y', alpha=0.1, linestyle='-', linewidth=0.5, color='#e5e7eb')
    
    # Plot 1: Delays over months
    ax1.plot(range(len(temporal_df)), temporal_df['Avg_Delay'].values, 
             color=colors['accent'], linewidth=2.5, marker='o', markersize=6, 
             markerfacecolor='white', markeredgewidth=2)
    ax1.fill_between(range(len(temporal_df)), temporal_df['Avg_Delay'].values, 
                      alpha=0.1, color=colors['accent'])
    ax1.set_xticks(range(len(temporal_df)))
    ax1.set_xticklabels(month_labels, fontsize=9)
    ax1.set_ylabel('Avg Departure Delay (min)', fontsize=11, color=colors['secondary'])
    ax1.set_title('Seasonal Delay Trends', fontsize=12, fontweight=600, pad=15, loc='left')
    
    # Plot 2: Cancellations over months
    ax2.bar(range(len(temporal_df)), temporal_df['Cancellation_Rate'].values * 100,
            color=colors['danger'], alpha=0.75, edgecolor='white', linewidth=1)
    ax2.set_xticks(range(len(temporal_df)))
    ax2.set_xticklabels(month_labels, fontsize=9)
    ax2.set_ylabel('Cancellation Rate (%)', fontsize=11, color=colors['secondary'])
    ax2.set_title('Seasonal Cancellation Trends', fontsize=12, fontweight=600, pad=15, loc='left')
    
    plt.tight_layout()
    return fig

# ==================== STREAMLIT APP ====================

def main():
    # Header
    st.markdown("""
    <div style="padding-bottom: 2rem; border-bottom: 1px solid #e5e7eb; margin-bottom: 2rem;">
        <h1 style="font-size: 2.5rem; font-weight: 300; margin-bottom: 0.5rem;">✈️ Flight Analytics</h1>
        <p style="color: #6b7280; font-size: 0.95rem; margin: 0;">Distributed analysis of airline performance metrics using PySpark</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load sample data (in production, load from cache)
    @st.cache_data
    def load_data():
        """Load or generate sample data for demonstration"""
        # For demo: generate synthetic data matching the analytics engine output
        np.random.seed(42)
        
        airlines = ["American Airlines", "Delta Air Lines", "Southwest Airlines", "United Airlines", 
                   "JetBlue Airways", "Alaska Airlines", "Spirit Airlines", "Frontier Airlines",
                   "Hawaiian Airlines", "Endeavor Air", "SkyWest Airlines", "Envoy Air",
                   "Republic Airways", "Allegiant Air", "PSA Airlines"]
        
        benchmark_data = []
        for airline in airlines:
            benchmark_data.append({
                'Airline': airline[:2].upper(),
                'Airline_Name': airline,
                'Total_Flights': np.random.randint(1000, 15000),
                'Avg_Departure_Delay': np.random.uniform(5, 25),
                'Avg_Arrival_Delay': np.random.uniform(3, 22),
                'P75_Departure_Delay': np.random.uniform(15, 45),
                'P95_Departure_Delay': np.random.uniform(35, 80),
                'Cancellation_Rate': np.random.uniform(0.005, 0.025),
                'Delay_StdDev': np.random.uniform(20, 50)
            })
        
        benchmark_df = pd.DataFrame(benchmark_data)
        
        # Temporal data
        temporal_data = []
        for month in range(1, 13):
            temporal_data.append({
                'Month': month,
                'Total_Flights': np.random.randint(80000, 120000),
                'Avg_Delay': np.random.uniform(8, 18),
                'Avg_Arrival_Delay': np.random.uniform(6, 16),
                'P75_Delay': np.random.uniform(20, 40),
                'Cancellation_Rate': np.random.uniform(0.008, 0.020),
                'Delay_StdDev': np.random.uniform(25, 50),
                'Travel_Score': np.random.uniform(8, 18)
            })
        
        temporal_df = pd.DataFrame(temporal_data)
        
        # Airport data
        airports = [
            "ATL", "DFW", "DEN", "ORD", "LAX", "JFK", "SFO", "LAS", 
            "SEA", "MIA", "BOS", "LGA", "EWR", "IAH", "PHX"
        ]
        airport_data = []
        for i, airport in enumerate(airports):
            airport_data.append({
                'Origin_Airport': airport,
                'Origin_City': airport,
                'Origin_State': 'US',
                'Flight_Count': np.random.randint(200, 5000),
                'Avg_Departure_Delay': np.random.uniform(6, 20),
                'P90_Delay': np.random.uniform(20, 50),
                'Cancellation_Rate': np.random.uniform(0.005, 0.020)
            })
        
        airport_df = pd.DataFrame(airport_data)
        
        return benchmark_df, temporal_df, airport_df
    
    benchmark_df, temporal_df, airport_df = load_data()
    
    # ==================== KEY METRICS ====================
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Flights",
            f"{benchmark_df['Total_Flights'].sum():,}",
            border=True
        )
    
    with col2:
        avg_delay = benchmark_df['Avg_Departure_Delay'].mean()
        st.metric(
            "Avg Delay",
            f"{avg_delay:.1f}m",
            border=True
        )
    
    with col3:
        cancel_rate = benchmark_df['Cancellation_Rate'].mean() * 100
        st.metric(
            "Cancel Rate",
            f"{cancel_rate:.2f}%",
            border=True
        )
    
    with col4:
        best_airline = benchmark_df.loc[benchmark_df['Avg_Departure_Delay'].idxmin()]
        st.metric(
            "Best Airline",
            best_airline['Airline'],
            f"{best_airline['Avg_Departure_Delay']:.1f}m",
            border=True
        )
    
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    
    # ==================== TABS FOR DIFFERENT ANALYSES ====================
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Airline Performance",
        "📍 Airport Analysis",
        "📅 Travel Planning",
        "📈 Trends"
    ])
    
    # TAB 1: AIRLINE PERFORMANCE
    with tab1:
        st.markdown("<h3 style='font-size: 1.5rem; font-weight: 500; margin-top: 0;'>Airline Performance Benchmark</h3>", 
                   unsafe_allow_html=True)
        
        col_chart1, col_chart2 = st.columns([1.3, 1])
        
        with col_chart1:
            st.pyplot(plot_airline_performance(benchmark_df), use_container_width=True)
        
        with col_chart2:
            st.pyplot(plot_delay_distribution(benchmark_df), use_container_width=True)
        
        st.markdown("<h4 style='font-size: 1.1rem; font-weight: 500; margin-top: 2rem; margin-bottom: 1rem;'>Detailed Metrics</h4>", 
                   unsafe_allow_html=True)
        
        # Display table with conditional formatting
        display_df = benchmark_df.sort_values('Avg_Departure_Delay', ascending=False)[
            ['Airline_Name', 'Total_Flights', 'Avg_Departure_Delay', 'P95_Departure_Delay', 
             'Cancellation_Rate', 'Delay_StdDev']
        ].copy()
        display_df['Cancellation_Rate'] = (display_df['Cancellation_Rate'] * 100).round(2).astype(str) + '%'
        display_df['Total_Flights'] = display_df['Total_Flights'].astype(int)
        display_df.columns = ['Airline', 'Flights', 'Avg Delay (m)', 'P95 Delay (m)', 'Cancel Rate', 'Std Dev']
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    # TAB 2: AIRPORT ANALYSIS
    with tab2:
        st.markdown("<h3 style='font-size: 1.5rem; font-weight: 500; margin-top: 0;'>Airport Performance Analysis</h3>", 
                   unsafe_allow_html=True)
        
        st.pyplot(plot_airport_heatmap(airport_df), use_container_width=True)
        
        st.markdown("<h4 style='font-size: 1.1rem; font-weight: 500; margin-top: 2rem; margin-bottom: 1rem;'>Airport Details</h4>", 
                   unsafe_allow_html=True)
        
        airport_display = airport_df.sort_values('Flight_Count', ascending=False)[
            ['Origin_Airport', 'Origin_City', 'Flight_Count', 'Avg_Departure_Delay', 'P90_Delay', 'Cancellation_Rate']
        ].copy()
        airport_display['Cancellation_Rate'] = (airport_display['Cancellation_Rate'] * 100).round(2).astype(str) + '%'
        airport_display.columns = ['Airport', 'City', 'Flights', 'Avg Delay (m)', 'P90 Delay (m)', 'Cancel Rate']
        
        st.dataframe(airport_display, use_container_width=True, hide_index=True)
    
    # TAB 3: TRAVEL PLANNING
    with tab3:
        st.markdown("<h3 style='font-size: 1.5rem; font-weight: 500; margin-top: 0;'>Best Times to Travel</h3>", 
                   unsafe_allow_html=True)
        
        st.pyplot(plot_best_travel_months(temporal_df), use_container_width=True)
        
        st.markdown("<h4 style='font-size: 1.1rem; font-weight: 500; margin-top: 2rem; margin-bottom: 1rem;'>Travel Score Breakdown</h4>", 
                   unsafe_allow_html=True)
        
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        travel_display = temporal_df.copy()
        travel_display['Month'] = travel_display['Month'].apply(lambda x: months[int(x)-1])
        travel_display['Cancellation_Rate'] = (travel_display['Cancellation_Rate'] * 100).round(2).astype(str) + '%'
        travel_display = travel_display[['Month', 'Travel_Score', 'Avg_Delay', 'Cancellation_Rate', 'Delay_StdDev']]
        travel_display.columns = ['Month', 'Score', 'Avg Delay (m)', 'Cancel Rate', 'Std Dev']
        
        st.dataframe(travel_display, use_container_width=True, hide_index=True)
    
    # TAB 4: TRENDS
    with tab4:
        st.markdown("<h3 style='font-size: 1.5rem; font-weight: 500; margin-top: 0;'>Seasonal Trends & Patterns</h3>", 
                   unsafe_allow_html=True)
        
        st.pyplot(plot_temporal_trends(temporal_df), use_container_width=True)
        
        st.markdown("""
        <div style='background: #fafaf9; padding: 1.5rem; border: 1px solid #e5e7eb; border-radius: 6px; margin-top: 2rem;'>
            <p style='color: #1f2937; font-size: 0.95rem; margin: 0;'>
                <strong>Key Insights:</strong><br>
                • Summer months (June-August) show elevated delays and cancellation rates<br>
                • Winter months experience variable conditions affecting consistency<br>
                • Spring and Fall months offer the most reliable travel windows<br>
                • Historical volatility measured via delay standard deviation guides booking decisions
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div style='margin-top: 4rem; padding-top: 2rem; border-top: 1px solid #e5e7eb; text-align: center; color: #9ca3af; font-size: 0.85rem;'>
        <p>Built with PySpark distributed computing engine | Data: 2024 Flight Operations</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
