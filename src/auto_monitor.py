import subprocess
import sys
import time
from datetime import datetime

INTERVAL_SECONDS = 60

print("=" * 60)
print("AUTOMATIC NETWORK PERFORMANCE MONITOR")
print("=" * 60)
print(f"Monitoring interval: {INTERVAL_SECONDS} seconds")
print("Press Ctrl+C to stop monitoring.")
print("=" * 60)

try:
    while True:
        print(
            f"\nStarting monitoring cycle at "
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )

        subprocess.run(
            [sys.executable, "src/network_monitor.py"],
            check=False
        )

        print(f"\nNext monitoring cycle in {INTERVAL_SECONDS} seconds...")
        time.sleep(INTERVAL_SECONDS)

except KeyboardInterrupt:
    print("\n" + "=" * 60)
    print("Automatic monitoring stopped by user.")
    print("=" * 60)