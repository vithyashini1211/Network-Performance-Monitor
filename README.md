# 📡 Network Performance Monitor

A Python-based network monitoring system that measures network performance, stores monitoring data in MySQL, generates reports and graphs, and provides an interactive Streamlit dashboard.

## Features

- Monitor multiple network devices using ICMP ping
- Measure network latency
- Detect packet loss
- Track device ONLINE/OFFLINE status
- Store monitoring results in MySQL
- Automatically collect network measurements
- Generate CSV performance reports
- Generate latency graphs
- Display network statistics using a Streamlit dashboard
- Visualize latency history for monitored devices
- Secure database credentials using environment variables

## Technologies Used

- Python
- MySQL
- Streamlit
- Pandas
- Matplotlib
- MySQL Connector/Python
- python-dotenv

## Project Structure

```text
NetworkPerformanceMonitor/
│
├── database/
│
├── reports/
│
├── src/
│   ├── auto_monitor.py
│   ├── dashboard.py
│   ├── db_connection.py
│   ├── generate_graph.py
│   ├── generate_report.py
│   └── network_monitor.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

## Monitored Devices

The current configuration monitors:

| Device | IP Address |
|---|---|
| Default Gateway | Local gateway |
| Google DNS | 8.8.8.8 |
| Cloudflare DNS | 1.1.1.1 |

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd Network-Performance-Monitor
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=network_monitoring
```

The `.env` file is ignored by Git and should not be committed.

## Running the Monitor

Run a network measurement:

```bash
python src/network_monitor.py
```

Run automatic monitoring:

```bash
python src/auto_monitor.py
```

## Generate Reports

Generate a CSV performance report:

```bash
python src/generate_report.py
```

Generate a latency graph:

```bash
python src/generate_graph.py
```

## Run the Dashboard

Start the Streamlit dashboard:

```bash
streamlit run src/dashboard.py
```

Then open the local Streamlit address displayed in the terminal.

## Dashboard

The dashboard displays:

- Total monitored devices
- Online devices
- Offline devices
- Current device status
- IP addresses
- Latency
- Packet loss
- Monitoring timestamps
- Latency history visualization

## Security

Database credentials are stored using environment variables rather than being hard-coded in the Python source code.

Sensitive files such as `.env` and the local virtual environment are excluded through `.gitignore`.