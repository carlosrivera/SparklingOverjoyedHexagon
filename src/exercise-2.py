import re
from datetime import datetime

'''
This task is to fix this code to write out a simple monthly report. The report should look professional.
The aim of the exercise is to:
- Ensure that the code works as specified including date formats
- Make sure the code will work correctly for any month
- Make sure the code is efficient
- Ensure adherence to PEP-8 and good coding standards for readability
- No need to add comments unless you wish to
- No need to add features to improve the output, but it should be sensible given the constraints of the exercise.
Code should display a dummy sales report
'''
# Do not change anything in the section below, it is just setting up some sample data
# test_data is a dictionary keyed on day number containing the date and
# sales figures for that day
month = "02"
test_data = {
    f"{x}": {
        "date": datetime.strptime(f"2021{month}{x:02d}", "%Y%m%d"),
        "sales": float(x ** 2 / 7)
    } for x in range(1, 29)
}
# Do not change anything in the section above, it is just setting up some
# sample data

# print(test_data)
#print(json.dumps(test_data, indent=2))

start = test_data["1"]  # range of days starts at 1
# end was missing one day, changed to dinamically set the end
end = test_data[str(len(test_data))]


def DateToDisplayDate(date: datetime) -> str:
    # E.g. Monday 8th February, 2021
    # refactored this function to call strftime only once, also 'th' was returned for all days
    # this sn't supported by default, so I've added a helper function _nth
    def _nth(n: str) -> str:
        t = int(n) % 10
        s = "st" if t == 1 else "nd" if t == 2 else "rd" if t == 3 else "th"

        # convert to int to remove leading 0's
        return f"{int(n)}{s}"

    date_formatted = f"{date.strftime('%a ~%d~ %B %Y')}"
    day = re.search(r"~(\d{1,2})~", date_formatted)

    if day:
        return re.sub(r"~(\d{1,2})~", f"{_nth(day.group(1))}", date_formatted)

    return date_formatted


# refactored the following for legibility
template = """
Sales Report
  Report start date:   {:>24s}   starting value: {:10.2f}
  Report end date:     {:>24s}   total sales:    {:10.2f}

Date                             Sales    Month to Date    Total Sales for the Month
""".format(
    DateToDisplayDate(start["date"]),
    start["sales"],
    DateToDisplayDate(end["date"]),
    end["sales"])

print(template)

total = 0

for k, v in enumerate(test_data):
    # converted month to int, as it was declared as string with a leading 0
    if int(month) == 2 and v == "29":
        print("Leap year")  # Must be displayed if data is for a leap year

    month_to_date = total
    total = test_data[v]["sales"] + total

    print(
        "{:>22s}    {:12.2f} {:14.2f} {:16.2f}".format(
            DateToDisplayDate(test_data[v]['date']),
            test_data[v]['sales'],
            month_to_date,
            total))
