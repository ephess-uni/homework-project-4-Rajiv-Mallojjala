# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict
import json

LATE_FEE_PER_DAY = 0.50


def read_json_file(file_path):
    with open(file_path) as file:
        data = json.load(file)
        return data if data else []


def reformat_dates(old_dates):
    return [datetime.strptime(date, '%Y-%m-%d').strftime('%d %b %Y') for date in old_dates]


def read_book_returns(infile):
    with open(infile, newline='') as f:
        reader = DictReader(f)
        return list(reader)


def date_range(start_date_str, n):
    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    except ValueError:
        raise ValueError(
            f"Invalid start date format: {start_date_str}. Expected format is yyyy-mm-dd.")

    try:
        return [start_date + timedelta(days=i) for i in range(n)]
    except OverflowError:
        raise ValueError(
            f"Invalid n value: {n}. Expected a non-negative integer.")


def add_date_range(values, start_date_str):
    dates = date_range(start_date_str, len(values))
    return list(zip(dates, values))


def fees_report(infile_path, outfile_path):
    data = read_json_file(infile_path)

    fees_report = []
    for patron in data['patrons']:
        if patron['fees'] > 0:
            fees_report.append({
                'patron_id': patron['patron_id'],
                'name': f"{patron['first_name']} {patron['last_name']}",
                'fees': f"{patron['fees']:.2f}"
            })

    with open(outfile_path, 'w') as f:
        json.dump(fees_report, f, indent=2)


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
