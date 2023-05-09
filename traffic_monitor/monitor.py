
import sys
import argparse
from typing import List, Tuple
from traffic_monitor.log import Log
from traffic_monitor.log_collection import LogCollection
from traffic_monitor.stats import stats
from traffic_monitor.alerts import check_high_traffic

TIME_OFFSET = 10

# List to store logs from last 2 minutes or custom defined window
log_window = LogCollection()

# Chunk of X seconds of logs (default 10 seconds)
log_chunk = LogCollection()


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
            check_high_traffic(log_window, args.threshold, zero_timestamp + TIME_OFFSET)

    # Print stats for last chunk
    stats(log_chunk)


if __name__ == '__main__':
    monitor()
