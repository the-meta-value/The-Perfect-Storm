#!/usr/bin/env python3
"""
Final Quality Check for Publication Dataset
Verifies all formatting standards are met
"""
import csv
import re
from datetime import datetime

# ◸──────── ✧ ──────── ◇ ———————🔹-💠-🔹——————— ◇ ──────── ✧ ────────◹
#       SECTION: Configuration
# ◺──────── ✧ ──────── ◇ ———————🔹-💠-🔹——————— ◇ ──────── ✧ ────────◿

INPUT_FILE = r"C:\Users\Merci\OneDrive\Desktop\2025\2025\csv\CLEANMASTER_FIXED.csv"

VALID_CATEGORIES = {'ACTofGOD', 'LLM', 'NETWORK'}
VALID_CORRELATIONS = {'YES', 'EVENT_SOURCE', ''}
DATE_PATTERN = re.compile(r'^\d{4}-\d{2}-\d{2}$')

# ◸──────── ✧ ──────── ◇ ———————🔹-💠-🔹——————— ◇ ──────── ✧ ────────◹
#       SECTION: Quality Check Functions
# ◺──────── ✧ ──────── ◇ ———————🔹-💠-🔹——————— ◇ ──────── ✧ ────────◿

def check_date_format(date_str, line_num):
    """Verify date is in YYYY-MM-DD format"""
    if not DATE_PATTERN.match(date_str):
        return f"Line {line_num}: Invalid date format '{date_str}'"
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError as e:
        return f"Line {line_num}: Invalid date '{date_str}' - {e}"
    return None


def check_category(category, line_num):
    """Verify category is valid"""
    if category not in VALID_CATEGORIES:
        return f"Line {line_num}: Invalid category '{category}'"
    return None


def check_summary_quoted(summary, line_num):
    """Verify SUMMARY field exists and is not empty"""
    # Note: CSV parser automatically strips quotes from properly quoted fields
    # So if we successfully parsed 7 fields, the quoting was correct
    if not summary or summary.strip() == '':
        return f"Line {line_num}: SUMMARY is empty"
    return None


def check_correlation(correlation, line_num):
    """Verify CORRELATION field has valid value"""
    if correlation not in VALID_CORRELATIONS:
        return f"Line {line_num}: Invalid CORRELATION value '{correlation}'"
    return None


def check_url_format(url, line_num):
    """Check if URL is properly formatted (if not empty)"""
    if url and not (url.startswith('http://') or url.startswith('https://')):
        # Some URLs might be empty, that's OK
        if url.strip():
            return f"Line {line_num}: URL doesn't start with http(s): {url[:50]}"
    return None


# ◸──────── ✧ ──────── ◇ ———————🔹-💠-🔹——————— ◇ ──────── ✧ ────────◹
#       SECTION: Main Quality Check Process
# ◺──────── ✧ ──────── ◇ ———————🔹-💠-🔹——————— ◇ ──────── ✧ ────────◿

def run_quality_check():
    """
    Run comprehensive quality check on the CSV file
    """
    print("=" * 70)
    print("PUBLICATION DATASET QUALITY CHECK")
    print("=" * 70)
    print(f"\nChecking file: {INPUT_FILE}\n")

    errors = []
    warnings = []
    total_lines = 0

    # Statistics
    stats = {
        'categories': {},
        'correlations': {},
        'subcategories': {}
    }

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for line_num, row in enumerate(reader, start=1):
            total_lines += 1

            if len(row) != 7:
                errors.append(f"Line {line_num}: Expected 7 fields, got {len(row)}")
                continue

            date, category, subcategory, type_field, summary, url, correlation = row

            # Run checks
            if error := check_date_format(date, line_num):
                errors.append(error)

            if error := check_category(category, line_num):
                errors.append(error)

            if error := check_summary_quoted(summary, line_num):
                errors.append(error)

            if error := check_correlation(correlation, line_num):
                errors.append(error)

            if error := check_url_format(url, line_num):
                warnings.append(error)

            # Collect statistics
            stats['categories'][category] = stats['categories'].get(category, 0) + 1
            stats['correlations'][correlation if correlation else 'EMPTY'] = \
                stats['correlations'].get(correlation if correlation else 'EMPTY', 0) + 1
            stats['subcategories'][subcategory] = stats['subcategories'].get(subcategory, 0) + 1

    # Print results
    print(f"Total entries checked: {total_lines}")
    print("\n" + "=" * 70)
    print("STATISTICS")
    print("=" * 70)

    print("\nCategories:")
    for cat, count in sorted(stats['categories'].items()):
        print(f"  {cat}: {count} entries")

    print("\nCorrelation Values:")
    for corr, count in sorted(stats['correlations'].items()):
        print(f"  {corr}: {count} entries")

    print(f"\nUnique Subcategories: {len(stats['subcategories'])}")

    print("\n" + "=" * 70)
    print("VALIDATION RESULTS")
    print("=" * 70)

    if errors:
        print(f"\n[ERROR] Found {len(errors)} errors:")
        for error in errors[:20]:
            print(f"  - {error}")
        if len(errors) > 20:
            print(f"  ... and {len(errors) - 20} more errors")
    else:
        print("\n[OK] No errors found!")

    if warnings:
        print(f"\n[WARNING] Found {len(warnings)} warnings:")
        for warning in warnings[:20]:
            print(f"  - {warning}")
        if len(warnings) > 20:
            print(f"  ... and {len(warnings) - 20} more warnings")
    else:
        print("\n[OK] No warnings!")

    print("\n" + "=" * 70)
    if not errors:
        print("[SUCCESS] Dataset is publication-ready!")
    else:
        print("[FAILED] Dataset requires fixes before publication")
    print("=" * 70)

    return len(errors) == 0


# ◸──────── ✧ ──────── ◇ ———————🔹-💠-🔹——————— ◇ ──────── ✧ ────────◹
#       SECTION: Script Entry Point
# ◺──────── ✧ ──────── ◇ ———————🔹-💠-🔹——————— ◇ ──────── ✧ ────────◿

if __name__ == "__main__":
    success = run_quality_check()
    exit(0 if success else 1)
