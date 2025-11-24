#!/usr/bin/env python3
"""
Verify field counts in CSV file
"""
import csv

INPUT_FILE = r"C:\Users\Merci\OneDrive\Desktop\2025\2025\csv\CLEANMASTER_FIXED.csv"

field_counts = {}
total = 0
errors = []

with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for line_num, row in enumerate(reader, start=1):
        total += 1
        field_count = len(row)
        field_counts[field_count] = field_counts.get(field_count, 0) + 1

        if field_count != 7:
            errors.append(f"Line {line_num}: {field_count} fields - {','.join(row[:3])}")

print(f"Total lines: {total}")
print("\nField count distribution:")
for count in sorted(field_counts.keys()):
    num = field_counts[count]
    status = "OK" if count == 7 else "ERROR"
    print(f"  {count} fields: {num} lines [{status}]")

if errors:
    print(f"\n{len(errors)} lines with incorrect field count:")
    for error in errors[:10]:  # Show first 10
        print(f"  {error}")
    if len(errors) > 10:
        print(f"  ... and {len(errors) - 10} more")
else:
    print("\n[OK] All lines have exactly 7 fields!")
