# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict

LATE_FEE_PER_DAY = 0.50


def reformat_dates(old_dates):
    reformatted_dates = []
    for date in old_dates:
        datetime_obj = datetime.strptime(date, '%Y-%m-%d')
        reformatted_dates.append(datetime_obj.strftime('%d %b %Y'))
    return reformatted_dates


def read_book_returns(infile):
    """Reads the book returns data from the input file and returns it as a
    list of dictionaries."""
    with open(infile, 'r', newline='') as f:
        reader = DictReader(f)
        return list(reader)


def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    try:
        start_date = datetime.strptime(start, '%Y-%m-%d')
    except ValueError:
        raise ValueError(
            f"Invalid start date format: {start}. Expected format is yyyy-mm-dd.")

    try:
        dates = [start_date + timedelta(days=i) for i in range(n)]
    except OverflowError:
        raise ValueError(
            f"Invalid n value: {n}. Expected a non-negative integer.")

    return dates


def add_date_range(values, start_date):
    dates = date_range(start_date, len(values))
    return list(zip(dates, values))


def fees_report(infile, outfile):
    """Calculates late fees per patron id and writes a summary report to
    outfile."""
    # Read the book returns data
    book_returns = read_book_returns(infile)

    # Create a dictionary to hold the fees for each patron
    patron_fees = defaultdict(float)

    # Loop through the book returns
    for row in book_returns:
        # Get the due date for the book
        due_date = row.get('due_date')
        if due_date is not None:
            due_date = datetime.strptime(due_date, '%Y-%m-%d')
        else:
            # Skip this row if there is no due date
            continue

        # Get the return date for the book
        return_date = datetime.strptime(row['return_date'], '%Y-%m-%d')

        # Calculate the number of days late
        days_late = (return_date - due_date).days
        if days_late <= 0:
            # No late fee if the book is returned on or before the due date
            continue

        # Calculate the late fee for the book
        late_fee = days_late * LATE_FEE_PER_DAY

        # Add the late fee to the patron's total
        patron_fees[row['patron_id']] += late_fee

    # Write the summary report to the output file
    with open(outfile, 'w', newline='') as f:
        writer = DictWriter(f, fieldnames=['patron_id', 'late_fee'])
        writer.writeheader()
        for patron_id, fee in patron_fees.items():
            writer.writerow({'patron_id': patron_id, 'late_fee': fee})


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

    # print(fees_report_out_short)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())
