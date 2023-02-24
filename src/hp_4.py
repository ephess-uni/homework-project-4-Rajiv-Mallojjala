# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(dates):
    return [datetime.strptime(d, '%Y-%m-%d').strftime('%d %b %Y') for d in dates]


def date_range(start, n):
    if not isinstance(start, str):
        raise TypeError('start should be a string in the format yyyy-mm-dd')
    if not isinstance(n, int):
        raise TypeError('n should be an integer')
    start_date = datetime.strptime(start, '%Y-%m-%d')
    return [start_date + timedelta(days=i) for i in range(n)]


def add_date_range(values, start_date):
    date_range_list = date_range(start_date, len(values))
    return [(date, value) for date, value in zip(date_range_list, values)]


def fees_report(infile, outfile):
    with open(infile) as f:
        reader = DictReader(f)
        late_fees_dict = {}
        for row in reader:
            patron_id = row['patron_id']
            date_due = datetime.strptime(row['date_due'], '%m/%d/%y')
            date_returned = datetime.strptime(row['date_returned'], '%m/%d/%y')
            if date_returned > date_due:
                days_late = (date_returned - date_due).days
                late_fees = round(0.25 * days_late, 2)
                if patron_id in late_fees_dict:
                    late_fees_dict[patron_id] += late_fees
                else:
                    late_fees_dict[patron_id] = late_fees
    with open(outfile, mode='w', newline='') as f:
        writer = writer(f)
        writer.writerow(['patron_id', 'late_fees'])
        for patron_id, fees in late_fees_dict.items():
            writer.writerow([patron_id, '{:.2f}'.format(fees)])


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
