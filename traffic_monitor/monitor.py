#

import argparse

def main():
    parser = argparse.ArgumentParser(description='HTTP traffic monitor from stdin or csv file')
    parser.add_argument('requests', type=str, help='HTTP requests', nargs='?')
    parser.add_argument('--file', type=str, help='Csv file path with HTTP requests')
    parser.add_argument('--threshold', type=str, help='Expected average requests per second')
    parser.add_argument('--timeout', type=int, help='Time limit to wait for new logs', default=60)

    args = parser.parse_args()

    print(f'requests: {args.requests}')
    print(f'threshold: {args.threshold}')

if __name__ == '__main__':
    main()