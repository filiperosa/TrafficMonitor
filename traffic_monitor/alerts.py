from typing import Tuple
from traffic_monitor.log_collection import LogCollection

# High traffic flag
high_traffic = False

# Timestamp of last alert
last_alert_timestamp = 0

def check_high_traffic(logs: LogCollection, threshold: int, zero_timestamp=None) -> Tuple[int, bool]:
    """Compute alerts for a list of logs"""
    
    global high_traffic
    global last_alert_timestamp

    # If no logs, return 0 requests per second
    if not len(logs):
        return (0, high_traffic)

    first_time = logs.get_oldest().timestamp
    last_time = logs.get_newest().timestamp
    exact_duration = 1
    if last_time != first_time:
        exact_duration = last_time - first_time
    
    requests_per_second = len(logs)/exact_duration

    if not zero_timestamp:
        zero_timestamp = first_time

    # If more than 1 second since last alert
    if last_time - last_alert_timestamp > 1:
        
        # Requests per second is above threshold
        if(not high_traffic and requests_per_second > threshold):
            print(f"High traffic generated an alert - hits = {len(logs)}, triggered at {last_time - zero_timestamp} seconds ({last_time})\n")
            high_traffic = True
        
        # Requests per second is back below threshold
        elif(high_traffic and requests_per_second <= threshold):
            print(f"High traffic alert recovered at {last_time - zero_timestamp} seconds ({last_time})\n")
            high_traffic = False
        
        last_alert_timestamp = last_time

    return (requests_per_second, high_traffic)