# ◸──────── ✧ ──────── ◇ ———————🔹-💠-🔹——————— ◇ ──────── ✧ ────────◹
#       SECTION: Event Correlation Analysis - ACTofGOD vs Tech Incidents
# ◺──────── ✧ ──────── ◇ ———————🔹-💠-🔹——————— ◇ ──────── ✧ ────────◿

import csv
from datetime import datetime, timedelta
from typing import List, Dict, Optional

def parse_date(date_str: str) -> Optional[datetime]:
    """Parse date string to datetime object."""
    try:
        return datetime.strptime(date_str.strip(), '%Y-%m-%d')
    except:
        return None

def find_actofgod_within_72_hours(event_date: datetime, actofgod_events: List[Dict]) -> Optional[str]:
    """
    Check if this event occurred within 72 hours AFTER an ACTofGOD event.

    Args:
        event_date: Date of the event to check
        actofgod_events: List of all ACTofGOD events

    Returns:
        String describing the ACTofGOD event if found, None otherwise
    """
    for act in actofgod_events:
        act_date = act['date']
        if act_date is None:
            continue

        # Check if event is AFTER the ACTofGOD event and within 72 hours
        time_diff = (event_date - act_date).total_seconds() / 3600  # hours

        if 0 <= time_diff <= 72:
            # Found a match - format the ACTofGOD event info
            hours_after = int(time_diff)
            act_info = f"{act['subcategory']} on {act['date'].strftime('%Y-%m-%d')}"
            return f"{hours_after}h after {act_info}"

    return None

def add_correlation_analysis(input_path: str, output_path: str) -> None:
    """
    Read CSV, analyze correlations, and add correlation column.

    Args:
        input_path: Path to input CSV
        output_path: Path to output CSV with correlation data
    """
    # Read all rows
    rows = []
    actofgod_events = []

    with open(input_path, 'r', encoding='utf-8', errors='replace', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

            # Collect ACTofGOD events
            if row.get('CATEGORY', '').strip().upper() == 'ACTOFGOD':
                event_date = parse_date(row.get('Event_Date', ''))
                if event_date:
                    actofgod_events.append({
                        'date': event_date,
                        'subcategory': row.get('SUBCATEGORY', '').strip(),
                        'summary': row.get('SUMMARY', '').strip()
                    })

    print(f"[OK] Found {len(actofgod_events)} ACTofGOD events")
    print(f"[OK] Analyzing {len(rows)} total events")

    # Sort ACTofGOD events by date for easier searching
    actofgod_events.sort(key=lambda x: x['date'])

    # Add correlation column to each row
    correlations_found = 0
    for row in rows:
        category = row.get('CATEGORY', '').strip().upper()
        event_date = parse_date(row.get('Event_Date', ''))

        if category == 'ACTOFGOD':
            # Mark as source event
            row['CORRELATION'] = 'SOURCE_EVENT'
        elif event_date:
            # Check if within 72 hours of an ACTofGOD event
            correlation = find_actofgod_within_72_hours(event_date, actofgod_events)
            row['CORRELATION'] = correlation if correlation else ''
            if correlation:
                correlations_found += 1
        else:
            row['CORRELATION'] = ''

    # Write output with new column
    fieldnames = ['EVENT_DATE', 'CATEGORY', 'SUBCATEGORY', 'SUMMARY', 'MISC', 'URL', 'CORRELATION']

    # Clean up rows to only include fields we want
    clean_rows = []
    for row in rows:
        clean_row = {field: row.get(field, '') for field in fieldnames}
        clean_rows.append(clean_row)

    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(clean_rows)

    print(f"[OK] Found {correlations_found} events within 72 hours of ACTofGOD events")
    print(f"[OK] Correlation analysis written to: {output_path}")

    # Print summary statistics
    print("\n[SUMMARY] ACTofGOD Events by Type:")
    event_types = {}
    for act in actofgod_events:
        subcat = act['subcategory']
        event_types[subcat] = event_types.get(subcat, 0) + 1

    for event_type, count in sorted(event_types.items()):
        print(f"  - {event_type}: {count} events")

# ◸──────── ✧ ──────── ◇ ———————🔹-💠-🔹——————— ◇ ──────── ✧ ────────◹
#       SECTION: Main Execution
# ◺──────── ✧ ──────── ◇ ———————🔹-💠-🔹——————— ◇ ──────── ✧ ────────◿

if __name__ == '__main__':
    input_file = r'C:\Users\Merci\OneDrive\Desktop\2025\2025\csv\NEWESTMASTER.csv'
    output_file = r'C:\Users\Merci\OneDrive\Desktop\2025\2025\csv\NEWESTMASTER_W_CORR.csv'

    try:
        add_correlation_analysis(input_file, output_file)
        print("\n[SUCCESS] Correlation analysis complete!")
        print(f"  Input: {input_file}")
        print(f"  Output: {output_file}")
        print("\nNew CORRELATION column shows:")
        print("  - 'SOURCE_EVENT' for ACTofGOD events")
        print("  - '[N]h after [EVENT] on [DATE]' for correlated events")
        print("  - Empty for events not within 72 hours of any ACTofGOD event")
        print("\nYou can now:")
        print("  1. Filter by CORRELATION column to see only correlated events")
        print("  2. Sort by Event_Date to see timeline")
        print("  3. Calculate correlation percentage")
    except Exception as e:
        print(f"[ERROR] Error during correlation analysis: {e}")
        import traceback
        traceback.print_exc()
