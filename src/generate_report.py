import csv
import os
from datetime import datetime

from db_connection import get_connection


def generate_report():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    print("=" * 60)
    print("NETWORK PERFORMANCE REPORT")
    print("=" * 60)

    cursor.execute("""
        SELECT
            d.device_name,
            d.ip_address,
            COUNT(p.metric_id) AS total_measurements,
            ROUND(AVG(p.latency_ms), 2) AS average_latency,
            ROUND(MIN(p.latency_ms), 2) AS minimum_latency,
            ROUND(MAX(p.latency_ms), 2) AS maximum_latency,
            ROUND(AVG(p.packet_loss_percent), 2) AS average_packet_loss
        FROM devices d
        LEFT JOIN performance_metrics p
            ON d.device_id = p.device_id
        GROUP BY d.device_id, d.device_name, d.ip_address
        ORDER BY d.device_id;
    """)

    results = cursor.fetchall()

    # Create reports directory if it does not exist
    os.makedirs("reports", exist_ok=True)

    # Create a unique report filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_file = f"reports/network_report_{timestamp}.csv"

    # Save report to CSV
    with open(report_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "Device Name",
            "IP Address",
            "Total Measurements",
            "Average Latency (ms)",
            "Minimum Latency (ms)",
            "Maximum Latency (ms)",
            "Average Packet Loss (%)"
        ])

        for row in results:
            writer.writerow([
                row["device_name"],
                row["ip_address"],
                row["total_measurements"],
                row["average_latency"],
                row["minimum_latency"],
                row["maximum_latency"],
                row["average_packet_loss"]
            ])

    print(f"\nReport saved to: {report_file}")

    # Display report in terminal
    for row in results:
        print()
        print(f"Device              : {row['device_name']}")
        print(f"IP Address          : {row['ip_address']}")
        print(f"Total Measurements  : {row['total_measurements']}")
        print(f"Average Latency     : {row['average_latency']} ms")
        print(f"Minimum Latency     : {row['minimum_latency']} ms")
        print(f"Maximum Latency     : {row['maximum_latency']} ms")
        print(f"Average Packet Loss : {row['average_packet_loss']}%")
        print("-" * 60)

    cursor.close()
    connection.close()


if __name__ == "__main__":
    generate_report()