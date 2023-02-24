# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(old_dates):
    new_dates = []
    for date_str in old_dates:
        date = datetime.strptime(date_str, '%Y-%m-%d')
        new_date_str = date.strftime('%d %b %Y')
        new_dates.append(new_date_str)
    return new_dates


def date_range(start, n):
    start_date = datetime.strptime(start, '%Y-%m-%d')
    dates = [start_date + timedelta(days=i) for i in range(n)]
    return dates


def add_date_range(values, start_date):
    dates = date_range(start_date, len(values))
    return list(zip(dates, values))


def fees_report(infile, outfile):
     # Open the input file and read the data
    with open(infile) as f:
        reader = DictReader(f)
        rows = [row for row in reader]

    # Group the rows by patron id
    rows_by_patron = defaultdict(list)
    for row in rows:
        rows_by_patron[row['patron_id']].append(row)

    # Calculate the late fees for each patron and write to the output file
    with open(outfile, 'w', newline='') as f:
        writer = DictWriter(f, fieldnames=['patron_id', 'late_fee'])
        writer.writeheader()

        for patron_id, rows in rows_by_patron.items():
            total_late_fee = 0

            for row in rows:
                due_date = datetime.strptime(row['due_date'], '%Y-%m-%d')
                return_date = datetime.strptime(row['return_date'], '%Y-%m-%d')

                if return_date > due_date:
                    days_late = (return_date - due_date).days
                    late_fee = days_late * float(row['fee_per_day'])
                    total_late_fee += late_fee

            writer.writerow(
                {'patron_id': patron_id, 'late_fee': total_late_fee})


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
