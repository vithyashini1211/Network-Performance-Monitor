import streamlit as st
import pandas as pd

from db_connection import get_connection


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Network Performance Monitor",
    page_icon="📡",
    layout="wide"
)

st.title("📡 Network Performance Monitor")
st.write("Real-time network monitoring dashboard")


# --------------------------------------------------
# CONNECT TO MYSQL
# --------------------------------------------------

connection = get_connection()
cursor = connection.cursor(dictionary=True)


# --------------------------------------------------
# GET LATEST DEVICE STATUS
# --------------------------------------------------

cursor.execute("""
    SELECT
        d.device_name,
        d.ip_address,
        p.status,
        p.latency_ms,
        p.packet_loss_percent,
        p.monitoring_time
    FROM devices d
    LEFT JOIN performance_metrics p
        ON d.device_id = p.device_id
    WHERE p.metric_id = (
        SELECT MAX(p2.metric_id)
        FROM performance_metrics p2
        WHERE p2.device_id = d.device_id
    )
    ORDER BY d.device_id;
""")

latest_results = cursor.fetchall()


# --------------------------------------------------
# GET LATENCY HISTORY
# --------------------------------------------------

cursor.execute("""
    SELECT
        d.device_name,
        p.monitoring_time,
        p.latency_ms
    FROM performance_metrics p
    JOIN devices d
        ON p.device_id = d.device_id
    WHERE p.latency_ms IS NOT NULL
    ORDER BY p.monitoring_time ASC;
""")

history_results = cursor.fetchall()


# Close database connection
cursor.close()
connection.close()


# --------------------------------------------------
# CONVERT RESULTS TO DATAFRAMES
# --------------------------------------------------

df = pd.DataFrame(latest_results)
history_df = pd.DataFrame(history_results)


# --------------------------------------------------
# NETWORK SUMMARY
# --------------------------------------------------

st.subheader("Network Summary")

total_devices = len(df)

if not df.empty:
    online_devices = len(df[df["status"] == "ONLINE"])
    offline_devices = len(df[df["status"] == "OFFLINE"])
else:
    online_devices = 0
    offline_devices = 0


col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Total Devices",
        value=total_devices
    )

with col2:
    st.metric(
        label="Online Devices",
        value=online_devices
    )

with col3:
    st.metric(
        label="Offline Devices",
        value=offline_devices
    )


st.divider()


# --------------------------------------------------
# CURRENT DEVICE STATUS
# --------------------------------------------------

st.subheader("Current Device Status")

if df.empty:

    st.warning("No monitoring data available.")

else:

    display_df = df.rename(
        columns={
            "device_name": "Device Name",
            "ip_address": "IP Address",
            "status": "Status",
            "latency_ms": "Latency (ms)",
            "packet_loss_percent": "Packet Loss (%)",
            "monitoring_time": "Monitoring Time"
        }
    )

    st.dataframe(
        display_df,
        width="stretch",
        hide_index=True
    )


st.divider()


# --------------------------------------------------
# LATENCY HISTORY CHART
# --------------------------------------------------

st.subheader("📈 Latency History")

if history_df.empty:
    st.warning("No latency history available.")

else:
    # Convert monitoring time to datetime
    history_df["monitoring_time"] = pd.to_datetime(
        history_df["monitoring_time"]
    )

    # IMPORTANT:
    # Convert MySQL DECIMAL values to normal Python floats
    history_df["latency_ms"] = pd.to_numeric(
        history_df["latency_ms"],
        errors="coerce"
    ).astype(float)

    # Remove invalid/null latency values
    history_df = history_df.dropna(
        subset=["latency_ms"]
    )

    # Sort each device's measurements chronologically
    history_df = history_df.sort_values(
        by=["device_name", "monitoring_time"]
    )

    # Give each device measurement a sequence number
    history_df["measurement"] = (
        history_df.groupby("device_name").cumcount() + 1
    )

    # Create chart data
    latency_chart = history_df.pivot(
        index="measurement",
        columns="device_name",
        values="latency_ms"
    )

    # Make sure all chart columns are floats
    latency_chart = latency_chart.astype(float)

    st.line_chart(
        latency_chart,
        x_label="Measurement",
        y_label="Latency (ms)",
        width="stretch"
    )