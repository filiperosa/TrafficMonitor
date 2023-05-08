# Traffic Monitor

This project is an HTTP traffic monitor reading a csv file or stdin

## Requirements

pytest, python 3.7+

## Installation

Install package with pip inside a virtual environment

```bash
  $ python3.9 -m venv venv 
  $ source venv/bin/activate
  $ pip install .
```

#### Uninstall

```bash
  $ cd <INSTALL_DIR>
  $ source venv/bin/activate
  $ pip uninstall traffic_monitor
```
    

## Usage/Examples

Once installed and within the correct python environment we can run the traffic monitor as a command line tool.

```bash
monitor [-h] [--threshold THRESHOLD] [--timeout TIMEOUT] [--chunksize CHUNKSIZE] [--window WINDOW] [input_file]
```
```
positional arguments:
  input_file

optional arguments:
  -h, --help            show this help message and exit
  --threshold THRESHOLD
                        Expected average requests per second
  --timeout TIMEOUT     Time limit to wait for new logs
  --chunksize CHUNKSIZE
                        Duration of log chunks used for printing stats, default is 10 seconds
  --window WINDOW       Time window of logs kept in memory, default is 2 minute`
```
#### Examples
Passing a target CSV file as argument
```bash
$ monitor requests_file.csv
```

Forwarding to stdin
```bash
$ monitor < requests_file.csv
```
```bash
$ cat requests_file.csv | monitor
```


## Running Tests

To run tests, we can use pytest

```bash
  $ cd <PACKAGE_FOLDER>
  $ source venv/bin/activate
  $ pytest
```

## Potential Improvements

- Add plotting and more visual presentation of the stats (e.g.: like htop improves the interface of top)

- Maybe have an option to create matplotlib plots

- More test coverage

- Output statistics and alerts to files



## Authors

- [@filiperosa](https://www.github.com/filiperosa)

