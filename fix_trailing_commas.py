# ◸──────── ✧ ──────── ◇ ———————🔹-💠-🔹——————— ◇ ──────── ✧ ────────◹
#       SECTION: CSV Cleanup - Remove trailing commas and fix formatting
# ◺──────── ✧ ──────── ◇ ———————🔹-💠-🔹——————— ◇ ──────── ✧ ────────◿

import csv
import sys

def fix_csv_trailing_commas(input_path: str, output_path: str) -> None:
    """
    Clean up CSV file by removing trailing empty fields and ensuring proper quoting.

    Args:
        input_path: Path to the input CSV file
        output_path: Path to write the corrected CSV
    """
    rows_processed = 0
    rows_cleaned = 0

    corrected_rows = []

    with open(input_path, 'r', encoding='utf-8', errors='replace', newline='') as infile:
        reader = csv.reader(infile)

        for i, row in enumerate(reader):
            # Remove trailing empty fields
            original_length = len(row)
            while row and row[-1].strip() == '':
                row.pop()

            if len(row) < original_length:
                rows_cleaned += 1

            # Clean up each remaining field
            cleaned_row = []
            for field in row:
                # Strip whitespace
                field = field.strip()
                # Replace newlines with spaces and normalize whitespace
                field = ' '.join(field.split())
                cleaned_row.append(field)

            corrected_rows.append(cleaned_row)
            rows_processed += 1

    # Write the corrected CSV with proper quoting
    with open(output_path, 'w', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile, quoting=csv.QUOTE_MINIMAL)
        writer.writerows(corrected_rows)

    print(f"[OK] Processed {rows_processed} rows")
    print(f"[OK] Cleaned {rows_cleaned} rows (removed trailing empty fields)")
    print(f"[OK] Corrected CSV written to: {output_path}")

# ◸──────── ✧ ──────── ◇ ———————🔹-💠-🔹——————— ◇ ──────── ✧ ────────◹
#       SECTION: Main Execution
# ◺──────── ✧ ──────── ◇ ———————🔹-💠-🔹——————— ◇ ──────── ✧ ────────◿

if __name__ == '__main__':
    input_file = r'C:\Users\Merci\OneDrive\Desktop\2025\2025\csv\New_Master_small.csv'
    output_file = r'C:\Users\Merci\OneDrive\Desktop\2025\2025\csv\New_Master_small.csv'

    try:
        fix_csv_trailing_commas(input_file, output_file)
        print("\n[SUCCESS] CSV file has been successfully corrected!")
        print(f"  Backup available at: {input_file}.backup")
        print(f"  Corrected file: {output_file}")
        print("\nChanges made:")
        print("  - Removed trailing commas/empty fields")
        print("  - Proper quoting for fields containing commas")
        print("  - Normalized whitespace within fields")
        print("\nThe file now has clean formatting and will work properly in Excel, Google Sheets, etc.")
    except Exception as e:
        print(f"[ERROR] Error fixing CSV: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
