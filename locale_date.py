#!/usr/bin/env python3
import datetime as dt
import locale

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')  # Set locale to US English

start = dt.date(2023, 10, 1)
end = dt.date(2023, 10, 31)
delta = end - start
print(f"Number of days in October 2023: {delta.days + 1}") 
print(f"start :{start.strftime('%A-%d-%m-%Y')}")
print(f"start :{end.strftime('%A-%d-%m-%Y')}")

year = start.year
month = start.month
day = start.day
print(f"Day: {day}, Year: {year}, Month: {month}")
print(f"Year: {year}, Month: {month}")

locale = dt.datetime.now()
utc = dt.datetime.now(dt.timezone.utc)
print(f"Local time: {locale.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"UTC time: {utc.strftime('%Y-%m-%d %H:%M:%S')}")