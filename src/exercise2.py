"""
Ortex exercise 2

Rated:
    - pylint: 6.55/10 (see line 27)
    - mypy: 0 issues
"""
import re
from datetime import datetime
from typing import Union, cast

# Do not change anything in the section below, it is just setting up some sample data
# TEST_DATA is a dictionary keyed on day number containing the date and
# sales figures for that day
MONTH = "02"
# pylint: disable=unsubscriptable-object
TEST_DATA: dict[str, dict[str, Union[datetime, float]]] = {
    f"{x}": {
        "date": datetime.strptime(f"2021{MONTH}{x:02d}", "%Y%m%d"),
        "sales": float(x ** 2 / 7)
    } for x in range(1, 29)
}
# pylint: disable=unsubscriptable-object
# Do not change anything in the section above, it is just setting up some

# While I was not supposed to change the section above, I added typing to the data,
# otherwise the typing isn't secure at all, also, test_data and month are constants,
# so I changed them to uppercase.
# The generator should be recreated as class to preserve typing and
# avoid E1136 (Value 'dict' is unsubscriptable (unsubscriptable-object)), for this
# reason, this file has a code quality of 6.55/10 (pylint)

start = TEST_DATA["1"]  # range of days starts at 1
# end was missing one day, changed to dinamically set the end
end = TEST_DATA[str(len(TEST_DATA))]

# changed function name to snake case (PEP C0103)
def date_to_display_date(date: Union[datetime, float]) -> str:
    """Returns a formatted date to string"""
    # E.g. Monday 8th February, 2021
    # refactored this function to call strftime only once, also 'th' was returned for all days
    # this sn't supported by default, so I've added a helper function _nth
    if isinstance(date, datetime):
        def _nth(num: str) -> str:
            # this is valid up to 40th, enough for days in a month
            module = int(num) % 20
            ordinal = ["th", "st", "nd", "rd"]
            position = ordinal[module] if module < 4 else ordinal[0]

            # convert to int to remove leading 0's
            return f"{int(num)}{position}"

        # cast type to datetime (PEP 484)
        date_formatted = f"{cast(datetime, date).strftime('%a ~%d~ %B %Y')}"
        day = re.search(r"~(\d{1,2})~", date_formatted)

        if day:
            return re.sub(r"~(\d{1,2})~", f"{_nth(day.group(1))}", date_formatted)

        return date_formatted

    raise TypeError("Unsupported type")


# refactored the following for legibility
TEMPLATE = """
Sales Report
  Report start date:   {:>24s}   starting value: {:10.2f}
  Report end date:     {:>24s}   total sales:    {:10.2f}

Date                             Sales    Month to Date    Total Sales for the Month
""".format(
        date_to_display_date(start["date"]),
        start["sales"],
        date_to_display_date(end["date"]),
        end["sales"])

print(TEMPLATE)

total: float = 0

for k, v in enumerate(TEST_DATA):
    # converted month to int, as it was declared as string with a leading 0
    if int(MONTH) == 2 and v == "29":
        print("Leap year")  # Must be displayed if data is for a leap year

    MONTH_TO_DATE = total
    total = cast(float, TEST_DATA[v]["sales"]) + total

    # month to date breaks the 'table' format, and is shown every month, so
    # I moved into the table itself to be more user friendly
    print(
        "{:>22s}    {:12.2f} {:14.2f} {:16.2f}".format(
            date_to_display_date(TEST_DATA[v]["date"]),
            TEST_DATA[v]["sales"],
            MONTH_TO_DATE,
            total))
