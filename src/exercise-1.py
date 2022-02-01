from calendar import monthrange
import csv
import collections
from datetime import datetime as dt
from typing import Any

colors = {
    'MAGENTA': '\033[95m',
    'BOLD': '\033[1m',
    'RESET': '\033[0m'
}

def unique(input_list: list) -> list:
    return (list(set(input_list)))


def print_eda(title: str = "", data: Any = None) -> None:
    if __debug__:
        print(f"\n{title}:\n", data)


def open_data(filename: str = "data/2017.csv"):
    with open(filename) as file:
        csv_reader = csv.reader(file, delimiter=',')

        headers = []
        df = []

        for line, row in enumerate(csv_reader):
            if line == 0:
                headers = row
            else:
                df.append(row)

    return headers, df


def question_one(h: list, df: list) -> None:
    # To answer this one, I pulled a list with the 'exchange' comlumn using a comprehension,
    # then get the most frequent one using a counter
    exchange, _ = collections.Counter(
        [r[len(h) - 1] for r in df]).most_common(1)[0]

    print(
        f"\n{colors['MAGENTA']}Most common exchange:\n{colors['RESET']}{exchange}")


def question_two(h: list, df: list) -> None:
    start_date = dt.strptime("08/01/2017", "%m/%d/%Y")
    end_date = dt.strptime("08/31/2017", "%m/%d/%Y")

    # Created a filter using the tradeddate colum
    def _f(d: list) -> bool:
        date = dt.strptime(d[len(h) - 14], "%Y%m%d")
        return date >= start_date and date <= end_date

    # Constructed a date filtered list of {company_name: valueEUR} objects
    values = [{r[2]: float(r[len(h) - 8])} for r in filter(_f, df)]

    # Aggeregate values with the same key using a counter
    counter = collections.Counter()
    for r in values:
        counter.update(r)

    # Search for the one with the highest value
    company, _ = counter.most_common(1)[0]

    print(
        f"\n{colors['MAGENTA']}Company with highest combined valueEUR in August 2017:\n{colors['RESET']}{company}")


def question_three(h: list, df: list) -> None:
    start_date: dt = dt.strptime("01/01/2017", "%m/%d/%Y")
    end_date: dt = dt.strptime("12/31/2017", "%m/%d/%Y")

    def _f(d: list) -> bool:
        date = dt.strptime(d[len(h) - 14], "%Y%m%d")
        return date >= start_date and date <= end_date and int(d[len(h) - 4]) == 3

    # filter all transactions from 2017 with a tradeSignificance of 3
    transactions = [t[len(h) - 14] for t in filter(_f, df)]
    # get the total count
    total = len(transactions)

    print(
        f"\n{colors['MAGENTA']}Monthly percentage of transactions with tradeSignificance 3:{colors['RESET']}")
    for m in range(1, 13):
        days = monthrange(2017, m)[1] # get current's month total days
        start_date: dt = dt.strptime(f"{m}/01/2017", "%m/%d/%Y")
        end_date: dt = dt.strptime(f"{m}/{days}/2017", "%m/%d/%Y")

        # create a filter to query current month transactions
        def _f(d: list) -> bool:
            date = dt.strptime(d, "%Y%m%d")
            return date >= start_date and date <= end_date

        # filter the transactions list and compute the percentage
        print("{}, {:5.2f}%".format(
            dt.strptime(f"{m}/01/2017", "%m/%d/%Y").strftime("%b"),
            len([t for t in filter(_f, transactions)])/total*100))


h, df = open_data()

question_one(h, df)
question_two(h, df)
question_three(h, df)
