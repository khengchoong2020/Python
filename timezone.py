#!/usr/bin/env python3
from datetime import datetime,timezone, timedelta

zones =(
    "Asia/Hong_kong",
    "America/New_York",
    "Europe/London",
    "Europe/Paris",''
)

for zone in zones:
    if zone:
        tz = timezone(timedelta(hours=8)) if zone == "Asia/Hong_kong" else timezone.utc
        now = datetime.now(tz)
        print(f"Current time in {zone}: {now.strftime('%Y-%m-%d %H:%M:%S')}")  # Format the output
    else:
        print("No timezone specified.")