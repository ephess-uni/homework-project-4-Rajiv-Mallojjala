# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
import csv
from collections import defaultdict


def reformat_dates(old_dates):
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001."""
    new_dates = []
    for date in old_dates:
        new_date = datetime.strptime(date, "%Y-%m-%d").strftime("%d %b %Y")
        new_dates.append(new_date)
    return new_dates


def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    start_date = datetime.strptime(start, '%Y-%m-%d')
    return [start_date + timedelta(days=i) for i in range(n)]


def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""
    date_range_list = date_range(start_date, len(values))
    return list(zip(date_range_list, values))


def read_book_returns(file_path):
    """Reads the book returns file and returns a list of dictionaries."""
    with open(file_path, 'r') as f:
        reader = DictReader(f)
        return list(reader)


def fees_report(infile, outfile):
    # open input and output files
    with open(infile, 'r') as csv_file_in, open(outfile, 'w', newline='') as csv_file_out:
        # create csv reader and writer objects
        reader = csv.DictReader(csv_file_in)
        writer = csv.DictWriter(csv_file_out, fieldnames=[
                                'patron_id', 'late_fees'])

        # create dictionary to keep track of late fees by patron_id
        late_fees = {}

        # iterate over rows in input file and calculate late fees
        for row in reader:
            # calculate number of days late
            date_due = datetime.strptime(row['date_due'], '%m/%d/%y')
            date_returned = datetime.strptime(row['date_returned'], '%m/%d/%y')
            days_late = (date_returned - date_due).days

            # calculate late fee and add to dictionary
            if days_late > 0:
                patron_id = row['patron_id']
                late_fee = days_late * 0.25
                if patron_id not in late_fees:
                    late_fees[patron_id] = late_fee
                else:
                    late_fees[patron_id] += late_fee

        # write summary report to output file
        writer.writeheader()
        for patron_id, late_fee in late_fees.items():
            writer.writerow({'patron_id': patron_id, 'late_fees': late_fee})
            
# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.


if __name__ == '__main__':
    
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    # BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())
