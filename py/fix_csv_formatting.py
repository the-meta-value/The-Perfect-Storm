#!/usr/bin/env python3
"""
CSV Dataset Formatter for Publication
Fixes unquoted SUMMARY fields and cleans CORRELATION field contamination
"""

import re
from pathlib import Path

# ◸──────── ✧ ──────── ◇ ———————🔹-💠-🔹——————— ◇ ──────── ✧ ────────◹
#       SECTION: Configuration and Setup
# ◺──────── ✧ ──────── ◇ ———————🔹-💠-🔹——————— ◇ ──────── ✧ ────────◿

INPUT_FILE = r"C:\Users\Merci\OneDrive\Desktop\2025\2025\csv\CLEANMASTER11202025.csv"
OUTPUT_FILE = r"C:\Users\Merci\OneDrive\Desktop\2025\2025\csv\CLEANMASTER_FIXED.csv"
BACKUP_FILE = r"C:\Users\Merci\OneDrive\Desktop\2025\2025\csv\CLEANMASTER11202025.csv.backup"

# Valid CORRELATION values
VALID_CORRELATIONS = {'YES', 'EVENT_SOURCE', ''}

# ◸──────── ✧ ──────── ◇ ———————🔹-💠-🔹——————— ◇ ──────── ✧ ────────◹
#       SECTION: CSV Line Parser and Fixer
# ◺──────── ✧ ──────── ◇ ———————🔹-💠-🔹——————— ◇ ──────── ✧ ────────◿

def parse_and_fix_line(line: str, line_num: int) -> str:
    """
    Parse a CSV line and fix formatting issues.

    Expected format: DATE,CATEGORY,SUBCATEGORY,TYPE,"SUMMARY",URL,CORRELATION

    Args:
        line: The CSV line to process
        line_num: Line number for error reporting

    Returns:
        Properly formatted CSV line
    """
    line = line.rstrip('\n\r')

    # Split by comma, but we need to handle quoted fields
    # First, let's do a naive split to count fields
    parts = line.split(',')

    # Expected structure:
    # parts[0] = DATE
    # parts[1] = CATEGORY
    # parts[2] = SUBCATEGORY
    # parts[3] = TYPE
    # parts[4...n-2] = SUMMARY (may be split if unquoted and contains commas)
    # parts[n-1] = URL
    # parts[n] = CORRELATION

    if len(parts) < 6:
        # Too few fields - this is an error
        print(f"Warning: Line {line_num} has only {len(parts)} fields: {line[:100]}")
        return line

    # Extract the fixed fields
    date = parts[0].strip()
    category = parts[1].strip()
    subcategory = parts[2].strip()
    type_field = parts[3].strip()

    # Now we need to figure out where SUMMARY ends
    # Strategy: Work backwards from the end
    # Last field is CORRELATION
    # Second-to-last is URL (usually starts with http or is empty)

    correlation = parts[-1].strip()

    # Check if correlation is valid; if not, it might be part of summary
    if correlation and not correlation.startswith('http') and correlation not in VALID_CORRELATIONS:
        # This might be bleeding from SUMMARY
        # Check if it ends with a quote (indicating it's the end of a quoted summary)
        if correlation.endswith('"'):
            # The entire summary was quoted but got split - reconstruct
            summary_parts = parts[4:]
            summary = ','.join(summary_parts)
            # Remove the trailing quote artifact
            summary = summary.rstrip('"').strip()
            # Re-quote properly
            summary = f'"{summary}"'
            url = ''
            correlation = ''
        else:
            # Likely: SUMMARY,URL,CORRELATION where SUMMARY has commas
            # Last field is CORRELATION (contaminated)
            # Second-to-last might be URL
            url = parts[-2].strip() if len(parts) > 5 else ''

            # Check if URL looks valid
            if url.startswith('http') or not url:
                # URL is valid, so everything from parts[4] to parts[-3] is SUMMARY
                summary_parts = parts[4:-2]
                summary = ','.join(summary_parts).strip()
                # Clean correlation - it got contaminated
                correlation = ''
            else:
                # URL is also contaminated - everything from parts[4] onward is SUMMARY
                summary_parts = parts[4:-1]
                summary = ','.join(summary_parts).strip()
                url = ''
                correlation = ''
    else:
        # Correlation looks valid
        # Now check URL
        url = parts[-2].strip() if len(parts) > 5 else ''

        # Everything between type and url is SUMMARY
        if len(parts) > 6:
            summary_parts = parts[4:-2]
            summary = ','.join(summary_parts).strip()
        else:
            summary = parts[4].strip() if len(parts) > 4 else ''

    # Now clean up the fields

    # Clean SUMMARY: ensure it's quoted
    if summary:
        # Remove any existing quotes first
        summary = summary.strip('"').strip()
        # Re-quote properly
        summary = f'"{summary}"'
    else:
        summary = '""'

    # Clean CORRELATION: only allow valid values
    if correlation not in VALID_CORRELATIONS:
        # Check if it's a URL (mistakenly placed)
        if correlation.startswith('http'):
            # This should probably be empty
            correlation = ''
        # Check if it contains quote marks or other artifacts
        elif '"' in correlation or 'Ap=' in correlation or 'Kp' in correlation:
            # This is contamination from SUMMARY
            correlation = ''
        elif correlation == '14155' or correlation == '1431 UTC':
            # These are artifacts
            correlation = ''
        else:
            # Unknown value - clear it to be safe
            print(f"Warning: Line {line_num} has unexpected CORRELATION value: '{correlation}' - clearing")
            correlation = ''

    # Reconstruct the line
    fixed_line = f"{date},{category},{subcategory},{type_field},{summary},{url},{correlation}"

    return fixed_line


# ◸──────── ✧ ──────── ◇ ———————🔹-💠-🔹——————— ◇ ──────── ✧ ────────◹
#       SECTION: Main Processing Function
# ◺──────── ✧ ──────── ◇ ———————🔹-💠-🔹——————— ◇ ──────── ✧ ────────◿

def process_csv():
    """
    Process the CSV file and fix all formatting issues.
    """
    print("Starting CSV formatting process...")
    print(f"Input file: {INPUT_FILE}")
    print(f"Output file: {OUTPUT_FILE}")

    # Create backup
    import shutil
    try:
        shutil.copy2(INPUT_FILE, BACKUP_FILE)
        print(f"[OK] Backup created: {BACKUP_FILE}")
    except Exception as e:
        print(f"Warning: Could not create backup: {e}")

    # Process file
    fixed_lines = []
    total_lines = 0
    fixed_count = 0

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, start=1):
            total_lines += 1
            original = line.rstrip('\n\r')
            fixed = parse_and_fix_line(line, line_num)

            if fixed != original:
                fixed_count += 1

            fixed_lines.append(fixed)

    # Write output
    with open(OUTPUT_FILE, 'w', encoding='utf-8', newline='') as f:
        for line in fixed_lines:
            f.write(line + '\n')

    print(f"\n[OK] Processing complete!")
    print(f"  Total lines processed: {total_lines}")
    print(f"  Lines modified: {fixed_count}")
    print(f"  Output written to: {OUTPUT_FILE}")


# ◸──────── ✧ ──────── ◇ ———————🔹-💠-🔹——————— ◇ ──────── ✧ ────────◹
#       SECTION: Script Entry Point
# ◺──────── ✧ ──────── ◇ ———————🔹-💠-🔹——————— ◇ ──────── ✧ ────────◿

if __name__ == "__main__":
    process_csv()
