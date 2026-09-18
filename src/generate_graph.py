import os
from datetime import datetime

import matplotlib.pyplot as plt

from db_connection import get_connection


def generate_latency_graph():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

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

    results = cursor.fetchall()

    cursor.close()
    connection.close()

    if not results:
        print("No latency data available.")
        return

    # Group measurements by device
    device_data = {}

    for row in results:
        device_name = row["device_name"]

        if device_name not in device_data:
            device_data[device_name] = {
                "times": [],
                "latencies": []
            }

        device_data[device_name]["times"].append(row["monitoring_time"])
        device_data[device_name]["latencies"].append(
            float(row["latency_ms"])
        )

    # Create graph
    plt.figure(figsize=(12, 6))

    for device_name, data in device_data.items():
        plt.plot(
            data["times"],
            data["latencies"],
            marker="o",
            label=device_name
        )

    plt.title("Network Latency Over Time")
    plt.xlabel("Monitoring Time")
    plt.ylabel("Latency (ms)")
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Create reports directory if needed
    os.makedirs("reports", exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    graph_file = f"reports/latency_graph_{timestamp}.png"

    plt.savefig(graph_file)
    plt.close()

    print("=" * 60)
    print("LATENCY GRAPH GENERATED")
    print("=" * 60)
    print(f"Graph saved to: {graph_file}")


if __name__ == "__main__":
    generate_latency_graph()