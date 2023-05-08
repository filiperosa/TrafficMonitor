#

import argparse
from typing import List
from traffic_monitor.log import Log
from datetime import datetime, timedelta

# Buffer to store logs from last 2 minutes
log_buffer: List[Log] = []

# Chunk of logs from last 10 seconds or given threshold 
log_chunk: List[Log] = []

def get_args() -> argparse.Namespace:
    """Parse command line arguments"""

    parser = argparse.ArgumentParser(description='HTTP traffic monitor from stdin or csv file')
    parser.add_argument('requests', type=str, help='HTTP requests', nargs='?')
    parser.add_argument('--file', type=str, help='CSV file path with HTTP requests')
    parser.add_argument('--threshold', type=str, help='Expected average requests per second', default=10)
    parser.add_argument('--timeout', type=int, help='Time limit to wait for new logs', default=60)

    return parser.parse_args()

def monitor():
    """Iterate over logs and compute stats and alerts"""

    args = get_args()

    print(f'requests: {args.requests}')
    print(f'threshold: {args.threshold}')
    print(f'file: {args.file}')

    with open(args.file, 'r') as f:
        f.readline()
        for line in f:
            values = [eval(value) for value in line.split(',')]
            log = Log(*values)

            # Remove logs older than 2 minutes from buffer
            while(len(log_buffer) and (log.timestamp - log_buffer[0].timestamp) > 120):
                log_buffer.pop(0)
            log_buffer.append(log)

            # If log_chunk is full, print stats end empty list
            if(len(log_chunk) and (log.timestamp - log_chunk[0].timestamp) > args.threshold):
                # TODO: Compute stats
                print(f"stats from {log_chunk[0].timestamp} to {log_chunk.pop().timestamp}")
                log_chunk.clear()
            log_chunk.append(log)
    # print(logs)
    print(log_buffer.pop())


if __name__ == '__main__':
    monitor()
