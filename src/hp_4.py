# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(old_dates):
    reformatted_dates = []
    for date in old_dates:
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        reformatted_dates.append(date_obj.strftime('%d %b %Y'))
    return reformatted_dates


def date_range(start, n):
    if not isinstance(start, str):
        raise TypeError("start must be a string in the format yyyy-mm-dd")
    if not isinstance(n, int):
        raise TypeError("n must be an integer")
    dates = []
    curr_date = datetime.strptime(start, '%Y-%m-%d')
    for i in range(n):
        dates.append(curr_date)
        curr_date += timedelta(days=1)
    return dates


def add_date_range(values, start_date):
    dates = date_range(start_date, len(values))
    return list(zip(dates, values))


def fees_report(infile, outfile):
    # Create an empty dictionary to store the late fees for each patron
    late_fees = {}

    # Open the input file for reading
    with open(infile, 'r') as f:
        # Read each line in the input file
        for line in f:
            # Split the line into fields
            fields = line.strip().split(',')
            
            # Extract the patron id, item type, and number of days late from the fields
            patron_id = fields[0]
            item_type = fields[1]
            days_late = int(fields[2])
            
            # Calculate the late fee for the item based on its type and number of days late
            if item_type == 'book':
                late_fee = days_late * 0.25
            elif item_type == 'dvd':
                late_fee = days_late * 0.50
            else:
                late_fee = days_late * 1.00
                
            # Add the late fee to the total for the patron
            if patron_id in late_fees:
                late_fees[patron_id] += late_fee
            else:
                late_fees[patron_id] = late_fee
                
    # Open the output file for writing
    with open(outfile, 'w') as f:
        # Write the header line to the output file
        f.write('Patron ID, Late Fee\n')
        
        # Write a line for each patron with late fees to the output file
        for patron_id, late_fee in late_fees.items():
            f.write('{}, {}\n'.format(patron_id, late_fee))


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
