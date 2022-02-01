"""
Ortex exercise 1

Rated:
    - pylint: 10/10
    - mypy: 0 issues
"""
from calendar import monthrange
import csv
import collections
from datetime import datetime as dt
from typing import Tuple

COLORS = {
    'MAGENTA': '\033[95m',
    'BOLD': '\033[1m',
    'RESET': '\033[0m'
}

def unique(input_list: list) -> list:
    """Uses a set to return unique elements in a list."""
    return list(set(input_list))


def open_data(filename: str = "data/2017.csv") -> Tuple[list, list]:
    """Reads a CSV file."""
    with open(filename, encoding="utf-8") as file:
        csv_reader = csv.reader(file, delimiter=',')

        headers: list = []
        rows: list = []

        for line, row in enumerate(csv_reader):
            if line == 0:
                headers = row
            else:
                rows.append(row)

    return headers, rows


def question_one(columns: list, rows: list) -> None:
    """
    Function to answer:
    What Exchange has had the most transactions in the file?
    """
    # To answer this one, I pulled a list with the 'exchange' comlumn
    # using a comprehension, then get the most frequent one using a counter
    exchange, _ = collections.Counter(
        [r[len(columns) - 1] for r in rows]).most_common(1)[0]

    print(
        f"\n{COLORS['MAGENTA']}Most common exchange:"\
        f"\n{COLORS['RESET']}{exchange}")


def question_two(columns: list, rows: list) -> None:
    """
    Function to answer:
    In August 2017, which companyName had the highest combined valueEUR?
    """
    start_date = dt.strptime("08/01/2017", "%m/%d/%Y")
    end_date = dt.strptime("08/31/2017", "%m/%d/%Y")

    # Created a filter using the tradeddate colum
    def _f(traded_date: list) -> bool:
        date = dt.strptime(traded_date[len(columns) - 14], "%Y%m%d")
        return (date >= start_date) & (date <= end_date)

    # Constructed a date filtered list of {company_name: valueEUR} objects
    values = [{r[2]: float(r[len(columns) - 8])} for r in filter(_f, rows)]

    # Aggeregate values with the same key using a counter
    counter: collections.Counter = collections.Counter()
    for row in values:
        counter.update(row)

    # Search for the one with the highest value
    company, _ = counter.most_common(1)[0]

    print(
        f"\n{COLORS['MAGENTA']}Company with highest combined valueEUR"\
        f"in August 2017:\n{COLORS['RESET']}{company}")


def question_three(columns: list, rows: list) -> None:
    """
    Function to answer:
    For 2017, only considering transactions with tradeSignificance 3,
    what is the percentage of transactions per month?
    """
    start_date: dt = dt.strptime("01/01/2017", "%m/%d/%Y")
    end_date: dt = dt.strptime("12/31/2017", "%m/%d/%Y")

    def _f(date: list) -> bool:
        str_date = dt.strptime(date[len(columns) - 14], "%Y%m%d")
        return (str_date >= start_date) & \
               (str_date <= end_date) & \
               (int(date[len(columns) - 4]) == 3)

    # filter all transactions from 2017 with a tradeSignificance of 3
    transactions: list = [t[len(columns) - 14] for t in filter(_f, rows)]
    # get the total count
    total = len(transactions)

    print(
        f"\n{COLORS['MAGENTA']}Monthly percentage of transactions"\
        f"with tradeSignificance 3:{COLORS['RESET']}")

    for month in range(1, 13):
        days = monthrange(2017, month)[1]  # get current's month total days
        _start_date: dt = dt.strptime(f"{month}/01/2017", "%m/%d/%Y")
        _end_date: dt = dt.strptime(f"{month}/{days}/2017", "%m/%d/%Y")

        # create a filter to query current month transactions
        def _fd(date: str, start=_start_date, end=_end_date) -> bool:
            str_date = dt.strptime(date, "%Y%m%d")
            return (str_date >= start) & (str_date <= end)

        formated_month = f"{month}/01/2017"
        # filter the transactions list and compute the percentage
        print(f"{dt.strptime(formated_month, '%m/%d/%Y').strftime(' % b')}, "\
              f"{len(list(filter(_fd, transactions)))/total*100:5.2f}%")


header, data_rows = open_data()

question_one(header, data_rows)
question_two(header, data_rows)
question_three(header, data_rows)
