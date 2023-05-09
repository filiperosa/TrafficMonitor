#
import sys
import argparse
from typing import List, Tuple
from traffic_monitor.log import Log
from traffic_monitor.log_collection import LogCollection

TIME_OFFSET = 10

# List to store logs from last 2 minutes or custom defined window
log_window = LogCollection()

# Chunk of X seconds of logs (default 10 seconds)
log_chunk = LogCollection()

# High traffic flag
high_traffic = False


def get_args() -> argparse.Namespace:
    """Parse command line arguments"""

    parser = argparse.ArgumentParser(description='HTTP traffic monitor from a csv file or stdin')
    parser.add_argument('input_file', type=argparse.FileType('r'), default=sys.stdin, nargs="?")
    parser.add_argument('--threshold', type=str, help='Expected average requests per second', default=10)
    parser.add_argument('--timeout', type=int, help='Time limit to wait for new logs', default=60)
    parser.add_argument('--chunksize', type=int, help='Duration of log chunks used for printing stats, default is 10 seconds', default=10)
    parser.add_argument('--window', type=int, help='Time window of logs kept in memory, default is 2 minutes', default=2)

    try:
        return parser.parse_args()
    except Exception as __:
        parser.print_help()
        exit(1)


def monitor():
    """Iterate over logs and compute stats and alerts"""

    # Timesamp of first log
    zero_timestamp = None
    
    args = get_args()

    with args.input_file as f:
        # Skip header
        f.readline()

        for line in f:
            values = [eval(value) for value in line.split(',')]
            log = Log(*values)

            # Only store relative timestamps to save memory
            if not zero_timestamp:
                zero_timestamp = log.timestamp - TIME_OFFSET
            log.timestamp -= zero_timestamp

            # Remove logs older than window minutes
            while(len(log_window) and (log.timestamp - log_window.get_oldest().timestamp) > args.window*60):
                log_window.pop_oldest()
            log_window.append(log)

            # If log_chunk is full, print stats end empty list
            if(len(log_chunk) and (log.timestamp - log_chunk.get_oldest().timestamp) > args.chunksize):
                stats(log_chunk)
                log_chunk.clear()
            log_chunk.append(log)

            # Compute alerts
            alerts(log_window, args.threshold)

    # Print stats for last chunk
    stats(log_chunk)


def stats(logs: LogCollection):
    """Compute stats for a list of logs"""

    sections = {}
    request_types = {}
    total_requests = len(logs)
    total_bytes = 0

    for log in logs:
        # Count hits per section
        if log.section in sections:
            sections[log.section] += 1
        else:
            sections[log.section] = 1

        # Count requests per type
        rtype = log.request.split()[0]
        if rtype in request_types:
            request_types[rtype] += 1
        else:
            request_types[rtype] = 1

        total_bytes += log.bytes

    # Sort sections by hits
    sections = {k: v for k, v in sorted(sections.items(), key=lambda item: item[1], reverse=True)}

    # Sort request types by hits
    request_types = {k: v for k, v in sorted(request_types.items(), key=lambda item: item[1], reverse=True)}

    first_time = logs.get_oldest().timestamp
    last_time = logs.get_newest().timestamp
    print(f"Stats from seconds {first_time} to {last_time} ({last_time - first_time} seconds)")

    print(f"Total requests: {total_requests}")
    print(f"Total bytes: {total_bytes}")
    
    print("Section hits:")
    for section, hits in sections.items():
        print(f"   {section}: {hits} hits, {hits/total_requests*100:.2f}%")

    print("Request types:")
    for rtype, hits in request_types.items():
        print(f"   {rtype}: {hits} hits, {hits/total_requests*100:.2f}%")

    print()
    

def alerts(logs: LogCollection, threshold: int) -> Tuple[int, bool]:
    """Compute alerts for a list of logs"""
    
    global high_traffic

    # If no logs, return 0 requests per second
    if not len(logs):
        return (0, high_traffic)

    first_time = logs.get_oldest().timestamp
    last_time = logs.get_newest().timestamp
    exact_duration = 1
    if last_time != first_time:
        exact_duration = last_time - first_time
    
    requests_per_second = len(logs)/exact_duration

    # Requests per second is above threshold
    if(not high_traffic and requests_per_second > threshold):
        print(f"High traffic generated an alert - hits = {len(logs)}, triggered at {last_time} seconds\n")
        high_traffic = True
    
    # Requests per second is back below threshold
    elif(high_traffic and requests_per_second <= threshold):
        print(f"High traffic alert recovered at {last_time} seconds\n")
        high_traffic = False

    return (requests_per_second, high_traffic)



if __name__ == '__main__':
    monitor()
