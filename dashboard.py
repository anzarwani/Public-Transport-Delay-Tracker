import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime, timedelta
from src.db import get_engine

def load_gold_data(engine):
    query = """
    SELECT route_id, hour, avg_delay, max_delay, count_delays
    FROM gold_route_delay_stats
    ORDER BY hour DESC
    """
    return pd.read_sql(query, engine)

def main():
    st.title("🚍 Public Transport Delay Tracker")

    engine = get_engine(st.secrets["database_url"])

    df = load_gold_data(engine)

    if df.empty:
        st.warning("No data available.")
        return

    df["hour"] = pd.to_datetime(df["hour"])

    # Sidebar filters
    st.sidebar.header("Filters")
    routes = df["route_id"].unique()
    selected_route = st.sidebar.selectbox("Select Route", options=routes)

    max_date = df["hour"].max()
    min_date = df["hour"].min()

    start_date = st.sidebar.date_input("Start Date", min_date)
    end_date = st.sidebar.date_input("End Date", max_date)

    # Filter dataframe based on selections
    filtered_df = df[
        (df["route_id"] == selected_route) &
        (df["hour"].dt.date >= start_date) &
        (df["hour"].dt.date <= end_date)
    ].sort_values("hour")

    if filtered_df.empty:
        st.warning("No data for selected filters.")
        return

    st.subheader(f"Delay Stats for Route: {selected_route}")

    # Summary stats
    st.markdown(f"""
    **Date range:** {start_date} to {end_date}  
    **Records:** {len(filtered_df)}  
    **Average delay (minutes):** {filtered_df['avg_delay'].mean():.2f}  
    **Maximum delay (minutes):** {filtered_df['max_delay'].max()}  
    """)

    # Line chart for average delay
    avg_delay_chart = alt.Chart(filtered_df).mark_line(point=True).encode(
        x="hour:T",
        y=alt.Y("avg_delay", title="Avg Delay (minutes)"),
        tooltip=["hour:T", "avg_delay"]
    ).properties(
        width=700,
        height=300,
        title="Average Delay Over Time"
    )

    # Line chart for max delay
    max_delay_chart = alt.Chart(filtered_df).mark_line(color="red", point=True).encode(
        x="hour:T",
        y=alt.Y("max_delay", title="Max Delay (minutes)"),
        tooltip=["hour:T", "max_delay"]
    ).properties(
        width=700,
        height=300,
        title="Maximum Delay Over Time"
    )

    st.altair_chart(avg_delay_chart, use_container_width=True)
    st.altair_chart(max_delay_chart, use_container_width=True)

if __name__ == "__main__":
    main()
