import mysql.connector
from ping3 import ping
import time

# ============================================
# DATABASE CONNECTION
# ============================================

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Abcd@1234",
    database="network_monitoring"
)

cursor = connection.cursor()


# ============================================
# GET DEVICES FROM DATABASE
# ============================================

cursor.execute("""
    SELECT device_id, device_name, ip_address
    FROM devices
""")

devices = cursor.fetchall()


print("=" * 60)
print("NETWORK PERFORMANCE MONITOR")
print("=" * 60)


# ============================================
# MONITOR EACH DEVICE
# ============================================

for device in devices:

    device_id = device[0]
    device_name = device[1]
    ip_address = device[2]

    print(f"\nChecking {device_name} ({ip_address})...")

    successful_pings = 0
    latencies = []

    # Send 5 ping requests
    for attempt in range(5):

        try:

            response = ping(ip_address, timeout=2)

            if response is not None:

                latency = response * 1000

                latencies.append(latency)

                successful_pings += 1

        except Exception as error:

            print(f"Ping error: {error}")

        time.sleep(0.2)


    # ========================================
    # CALCULATE PACKET LOSS
    # ========================================

    total_pings = 5

    lost_pings = total_pings - successful_pings

    packet_loss = (lost_pings / total_pings) * 100


    # ========================================
    # CALCULATE AVERAGE LATENCY
    # ========================================

    if successful_pings > 0:

        average_latency = sum(latencies) / len(latencies)

        average_latency = round(average_latency, 2)

        status = "ONLINE"

    else:

        average_latency = None

        status = "OFFLINE"


    # ========================================
    # DISPLAY RESULTS
    # ========================================

    print(f"Status      : {status}")

    if average_latency is not None:
        print(f"Avg Latency : {average_latency} ms")
    else:
        print("Avg Latency : N/A")

    print(f"Packet Loss : {packet_loss:.2f}%")

    print(
        f"Pings       : {successful_pings}/{total_pings} successful"
    )


    # ========================================
    # SAVE TO MYSQL
    # ========================================

    sql = """
        INSERT INTO performance_metrics
        (
            device_id,
            status,
            latency_ms,
            packet_loss_percent
        )
        VALUES (%s, %s, %s, %s)
    """

    values = (
        device_id,
        status,
        average_latency,
        packet_loss
    )

    cursor.execute(sql, values)

        # ========================================
    # ALERT DETECTION
    # ========================================

    alert_type = None
    alert_message = None
    severity = None

    # Device completely unreachable
    if packet_loss == 100:

        alert_type = "DEVICE DOWN"
        alert_message = f"{device_name} is unreachable."
        severity = "CRITICAL"

    # High packet loss
    elif packet_loss > 20:

        alert_type = "HIGH PACKET LOSS"
        alert_message = (
            f"{device_name} has {packet_loss:.2f}% packet loss."
        )
        severity = "WARNING"

    # High latency
    elif average_latency is not None and average_latency > 100:

        alert_type = "HIGH LATENCY"
        alert_message = (
            f"{device_name} latency is "
            f"{average_latency:.2f} ms."
        )
        severity = "WARNING"


    # Save alert if a problem was detected
    if alert_type is not None:

        alert_sql = """
            INSERT INTO alerts
            (
                device_id,
                alert_type,
                message,
                severity
            )
            VALUES (%s, %s, %s, %s)
        """

        alert_values = (
            device_id,
            alert_type,
            alert_message,
            severity
        )

        cursor.execute(alert_sql, alert_values)

        print(f"ALERT       : {alert_type}")


# ============================================
# SAVE DATABASE CHANGES
# ============================================

connection.commit()

cursor.close()

connection.close()


print("\n" + "=" * 60)
print("Monitoring completed.")
print("Results saved to MySQL.")
print("=" * 60)