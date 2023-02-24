# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
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
    """Calculates late fees per patron id and writes a summary report to
    outfile."""
    # Load book return data from input file
    with open(infile, 'r') as f:
        reader = DictReader(f)
        book_returns = list(reader)

    # Create dictionary to hold fees for each patron id
    fees_by_patron = defaultdict(float)

    # Calculate fees for each book return
    for row in book_returns:
        due_date = datetime.strptime(row['due_date'], '%Y-%m-%d')
        return_date = datetime.strptime(row['return_date'], '%Y-%m-%d')
        days_late = (return_date - due_date).days
        if days_late > 0:
            patron_id = row['patron_id']
            fee = days_late * 0.25
            fees_by_patron[patron_id] += fee

    # Write fees report to output file
    with open(outfile, 'w', newline='') as f:
        fieldnames = ['patron_id', 'total_fees']
        writer = DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for patron_id, total_fees in fees_by_patron.items():
            writer.writerow({'patron_id': patron_id, 'total_fees': total_fees})


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
