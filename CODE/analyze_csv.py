# ◸──────── ✧ ──────── ◇ ———————🔹-💠-🔹——————— ◇ ──────── ✧ ────────◹
#       SECTION: CSV Analysis Script - Count fields per row
# ◺──────── ✧ ──────── ◇ ———————🔹-💠-🔹——————— ◇ ──────── ✧ ────────◿

import csv

input_file = r'C:\Users\Merci\OneDrive\Desktop\2025\2025\csv\NEWESTMASTER.csv'

with open(input_file, 'r', encoding='utf-8', errors='replace', newline='') as f:
    reader = csv.reader(f)
    for i, row in enumerate(reader):
        if i < 10:  # Just show first 10 rows
            # Count non-empty fields
            non_empty = sum(1 for field in row if field.strip())
            print(f"Row {i}: {len(row)} fields ({non_empty} non-empty)")
            print(f"  Fields: {row}")
            print()
