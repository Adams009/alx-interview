#!/usr/bin/python3

import sys
import signal

def print_msg(dict_sc, total_file_size):
    """
    Method to print the metrics.
    Args:
        dict_sc: dict of status codes
        total_file_size: total of the file
    Returns:
        Nothing
    """
    print("File size: {}".format(total_file_size))
    for key in sorted(dict_sc.keys()):
        if dict_sc[key] > 0:
            print("{}: {}".format(key, dict_sc[key]))

def handle_interrupt(signal, frame):
    """
    Handle the keyboard interruption signal to print the current statistics.
    """
    print_msg(dict_sc, total_file_size)
    sys.exit(0)

# Initialize variables
total_file_size = 0
counter = 0
dict_sc = {"200": 0, "301": 0, "400": 0, "401": 0, "403": 0, "404": 0, "405": 0, "500": 0}

# Register the signal handler
signal.signal(signal.SIGINT, handle_interrupt)

try:
    for line in sys.stdin:
        parts = line.split()
        if len(parts) != 10:
            continue
        
        try:
            file_size = int(parts[-1])
            status_code = parts[-2]

            if status_code in dict_sc:
                dict_sc[status_code] += 1
                total_file_size += file_size
                counter += 1

            if counter == 10:
                print_msg(dict_sc, total_file_size)
                counter = 0

        except (ValueError, IndexError):
            continue

finally:
    print_msg(dict_sc, total_file_size)
