# ◸──────── ✧ ──────── ◇ ———————🔹-💠-🔹——————— ◇ ──────── ✧ ────────◹
#       SECTION: Rate-Based Correlation Analysis (Aurum's Method)
# ◺──────── ✧ ──────── ◇ ———————🔹-💠-🔹——————— ◇ ──────── ✧ ────────◿

"""
Analyzes COMBINED_MASTER.csv using Aurum's rate-based methodology:
Calculate incidents per day INSIDE vs OUTSIDE 72h windows after solar events.
"""

import csv
from datetime import datetime, timedelta
from collections import defaultdict

input_file = r'C:\Users\Merci\OneDrive\Desktop\2025\2025\csv\Continued\COMBINED_MASTER.csv'

# Load all events
solar_dates = []
incident_dates = []

with open(input_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        date = datetime.strptime(row['DATE'], '%Y-%m-%d')
        if row['CATEGORY'] == 'ACTofGOD':
            solar_dates.append(date)
        elif row['CATEGORY'] in ['LLM', 'NETWORK']:
            incident_dates.append(date)

print("=" * 70)
print("RATE-BASED CORRELATION ANALYSIS (Aurum's Method)")
print("=" * 70)
print(f"\nDataset: COMBINED_MASTER.csv")
print(f"Solar events (ACTofGOD): {len(solar_dates)}")
print(f"Tech incidents (LLM/NETWORK): {len(incident_dates)}")

# Get timeline
first_date = min(solar_dates + incident_dates)
last_date = max(solar_dates + incident_dates)
days_covered = (last_date - first_date).days + 1

print(f"Timeline: {first_date.strftime('%Y-%m-%d')} to {last_date.strftime('%Y-%m-%d')}")
print(f"Total days: {days_covered}")

# Create set of dates within 72h of solar events
solar_window_dates = set()
for solar_date in solar_dates:
    for hours in range(0, 73):  # 0-72 hours after
        check_date = solar_date + timedelta(hours=hours)
        if first_date <= check_date <= last_date:
            solar_window_dates.add(check_date.date())

# Count incidents per day
daily_incidents = defaultdict(int)
for incident_date in incident_dates:
    daily_incidents[incident_date.date()] += 1

# Separate days into "in window" vs "out of window"
incidents_in_window = []
incidents_out_window = []

current = first_date
while current <= last_date:
    date_key = current.date()
    incident_count = daily_incidents[date_key]

    if date_key in solar_window_dates:
        incidents_in_window.append(incident_count)
    else:
        incidents_out_window.append(incident_count)

    current += timedelta(days=1)

# Calculate statistics
days_in_window = len(incidents_in_window)
days_out_window = len(incidents_out_window)
total_incidents_in = sum(incidents_in_window)
total_incidents_out = sum(incidents_out_window)
mean_in = total_incidents_in / days_in_window if days_in_window > 0 else 0
mean_out = total_incidents_out / days_out_window if days_out_window > 0 else 0
irr = mean_in / mean_out if mean_out > 0 else 0

print("\n" + "=" * 70)
print("RESULTS - 72 HOUR WINDOW")
print("=" * 70)
print(f"\nDays within 72h of solar event: {days_in_window} ({days_in_window/days_covered*100:.1f}%)")
print(f"Days outside 72h window: {days_out_window} ({days_out_window/days_covered*100:.1f}%)")

print(f"\nIncidents INSIDE 72h windows: {total_incidents_in}")
print(f"Incidents OUTSIDE 72h windows: {total_incidents_out}")

print(f"\n--- INCIDENT RATE COMPARISON ---")
print(f"Mean incidents/day INSIDE windows:  {mean_in:.2f}")
print(f"Mean incidents/day OUTSIDE windows: {mean_out:.2f}")
print(f"Incident Rate Ratio (IRR):          {irr:.2f}")

if irr > 1.3:
    print("\n✓ STRONG CORRELATION: Incidents happen {:.0f}% MORE during solar activity".format((irr-1)*100))
elif irr > 1.1:
    print("\n~ WEAK CORRELATION: Incidents happen {:.0f}% more during solar activity".format((irr-1)*100))
elif irr > 0.9:
    print("\n= NO CORRELATION: Incident rate is similar inside and outside windows")
else:
    print("\n✗ ANTI-CORRELATION: Incidents happen LESS during solar activity")

print("\nNote: Aurum found IRR = 1.61 (61% higher rate) with p = 0.0007")
print("      on her dataset (Jan 15 - Nov 2, all LLM providers)")
