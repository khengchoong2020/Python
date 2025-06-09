#!/usr/bin/env python3
from datetime import datetime,timezone, timedelta

zones =(
    "Asia/Hong_kong",
    "America/New_York",
    "Europe/London",
    "Europe/Paris"
)

for zone in zones:
    tz = timezone.utc
    now = datetime.now(tz)
    print(f"Current time in {zone}: {now.strftime('%Y-%m-%d %H:%M:%S')}")  # Format the output
    print(f"Current time in {zone}: {now}")  # Format the output
