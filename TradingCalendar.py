from datetime import date
from datetime import timedelta
import dateutil.easter
import holidays


def isValidTradingDay(isodate, holidays):
    day = date.fromisoformat(isodate).isoweekday()
    status = holidays.get(isodate)
    if day==6 or day==7 or status!= None:
        return(False)
    else:
        return(True)


# Select country
def createHolidayCalendar(year):
    us_holidays = holidays.US(years=year)
    us_holidays.pop_named('Veterans Day')
    us_holidays.pop_named('Columbus Day')
    try:
        us_holidays.pop_named('Veterans Day (Observed)')
    except KeyError:
      pass
    try:
        us_holidays.pop_named('Columbus Day (Observed)')
    except KeyError:
        pass

    good_friday = dateutil.easter.easter(year) + timedelta(days=-2)

    us_holidays.append({good_friday:'Good Friday'})

    return(us_holidays)

print(isValidTradingDay('2020-05-25', createHolidayCalendar(2020)))
