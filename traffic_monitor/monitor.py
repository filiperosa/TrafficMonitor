#

import argparse
from typing import List
from traffic_monitor.log import Log
from datetime import datetime, timedelta

# Buffer to store logs from last 2 minutes
log_buffer: List[Log] = []

# Chunk of X seconds of logs (default 10 seconds)
log_chunk: List[Log] = []

def get_args() -> argparse.Namespace:
    """Parse command line arguments"""

    parser = argparse.ArgumentParser(description='HTTP traffic monitor from stdin or csv file')
    parser.add_argument('requests', type=str, help='HTTP requests', nargs='?')
    parser.add_argument('--file', type=str, help='CSV file path with HTTP requests')
    parser.add_argument('--threshold', type=str, help='Expected average requests per second', default=10)
    
    parser.add_argument('--timeout', type=int, help='Time limit to wait for new logs', default=60)
    parser.add_argument('--chunksize', type=int, help='Duration of log chunks used for printing stats, default is 10 seconds', default=10)
    parser.add_argument('--window', type=int, help='Time window of logs kept in memory, default is 2 minutes', default=2)

    
    return parser.parse_args()

def monitor():
    """Iterate over logs and compute stats and alerts"""

    args = get_args()

    with open(args.file, 'r') as f:
        f.readline()
        for line in f:
            values = [eval(value) for value in line.split(',')]
            log = Log(*values)

            # Remove logs older than 2 minutes from buffer
            while(len(log_buffer) and (log.timestamp - log_buffer[0].timestamp) > args.window*60):
                log_buffer.pop(0)
            log_buffer.append(log)

            # If log_chunk is full, print stats end empty list
            if(len(log_chunk) and (log.timestamp - log_chunk[0].timestamp) > args.chunksize):
                stats(log_chunk)
                log_chunk.clear()
            log_chunk.append(log)
    # print(logs)


def stats(logs: List[Log]):
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

    first_time = logs[0].timestamp
    last_time = logs[len(logs)-1].timestamp
    print(f"Stats from {first_time} to {last_time} ({last_time - first_time} seconds)")

    print(f"Total requests: {total_requests}")
    print(f"Total bytes: {total_bytes}")
    
    print("Section hits:")
    for section, hits in sections.items():
        print(f"   {section}: {hits} hits, {hits/total_requests*100:.2f}%")

    print("Request types:")
    for rtype, hits in request_types.items():
        print(f"   {rtype}: {hits} hits, {hits/total_requests*100:.2f}%")

    print()
    

def alerts(logs: List[Log]):
    """Compute alerts for a list of logs"""

    # Compute average requests per second
    # If average is above threshold, print alert
    # If average is below threshold, print recovery
    # If average is above threshold for more than 2 minutes, print high traffic alert

    # Whenever total traffic for the past 2 minutes exceeds a certain number on average, print a message to the console saying that “High traffic generated an alert - hits = {value}, triggered at {time}”. The default threshold should be 10 requests per second but should be configurable

    pass




if __name__ == '__main__':
    monitor()
