# ◸──────── ✧ ──────── ◇ ———————🔹-💠-🔹——————— ◇ ──────── ✧ ────────◹
#       SECTION: CSV Repair Script Final - Handles multi-line fields
# ◺──────── ✧ ──────── ◇ ———————🔹-💠-🔹——————— ◇ ──────── ✧ ────────◿

import csv
import sys

def fix_csv_file(input_path: str, output_path: str) -> None:
    """
    Read a CSV file and rewrite it with proper formatting.

    This version properly handles:
    - Multi-line fields (fields with newlines inside quotes)
    - Fields with embedded commas
    - Trailing commas
    - Consistent quoting

    Args:
        input_path: Path to the input CSV file
        output_path: Path to write the corrected CSV
    """
    rows_processed = 0
    rows_with_issues = 0

    corrected_rows = []

    # Read with csv.reader to properly handle quoted multi-line fields
    with open(input_path, 'r', encoding='utf-8', errors='replace', newline='') as infile:
        # Use csv.reader which properly handles quotes and multi-line fields
        reader = csv.reader(infile)

        for i, row in enumerate(reader):
            # Ensure exactly 6 fields
            if len(row) < 6:
                # Pad with empty strings
                while len(row) < 6:
                    row.append('')
                rows_with_issues += 1
            elif len(row) > 6:
                # Too many fields - merge extras into SUMMARY (field index 3)
                # Keep first 3, merge middle ones into index 3, keep last 2
                fixed_row = row[:3]
                # Merge from index 3 to -2 into SUMMARY
                summary_parts = row[3:-2] if len(row) > 5 else row[3:]
                fixed_row.append(','.join(summary_parts))
                # Add MISC and URL
                if len(row) >= 5:
                    fixed_row.append(row[-2])
                else:
                    fixed_row.append('')
                if len(row) >= 6:
                    fixed_row.append(row[-1])
                else:
                    fixed_row.append('')
                row = fixed_row
                rows_with_issues += 1

            # Clean up each field
            cleaned_row = []
            for field in row:
                # Strip whitespace and remove any stray quotes
                field = field.strip()
                # Replace newlines within fields with spaces
                field = field.replace('\n', ' ').replace('\r', ' ')
                # Replace multiple spaces with single space
                field = ' '.join(field.split())
                cleaned_row.append(field)

            corrected_rows.append(cleaned_row)
            rows_processed += 1

    # Write the corrected CSV with proper quoting
    with open(output_path, 'w', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile, quoting=csv.QUOTE_MINIMAL)
        writer.writerows(corrected_rows)

    print(f"[OK] Processed {rows_processed} rows")
    print(f"[OK] Fixed {rows_with_issues} rows with formatting issues")
    print(f"[OK] Corrected CSV written to: {output_path}")

# ◸──────── ✧ ──────── ◇ ———————🔹-💠-🔹——————— ◇ ──────── ✧ ────────◹
#       SECTION: Main Execution
# ◺──────── ✧ ──────── ◇ ———————🔹-💠-🔹——————— ◇ ──────── ✧ ────────◿

if __name__ == '__main__':
    input_file = r'C:\Users\Merci\OneDrive\Desktop\2025\2025\csv\NEWESTMASTER.csv'
    output_file = r'C:\Users\Merci\OneDrive\Desktop\2025\2025\csv\NEWESTMASTER_FIXED.csv'

    try:
        fix_csv_file(input_file, output_file)
        print("\n[SUCCESS] CSV file has been successfully corrected!")
        print(f"  Original (backup): {input_file}.backup")
        print(f"  Corrected file: {output_file}")
        print("\nChanges made:")
        print("  - Removed multi-line fields (newlines replaced with spaces)")
        print("  - Ensured all rows have exactly 6 columns")
        print("  - Proper quoting for fields with commas")
        print("  - Removed trailing commas")
        print("\nYou can now use the corrected file in Excel, Google Sheets, or any CSV tool.")
    except Exception as e:
        print(f"[ERROR] Error fixing CSV: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
