import csv

input_file = r'C:\Users\Merci\OneDrive\Desktop\2025\2025\csv\NEWESTMASTER_W_CORR.csv'

with open(input_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    correlated = [row for row in reader if row.get('CORRELATION', '') and row.get('CORRELATION', '') != 'SOURCE_EVENT']

print(f"[RESULTS] Found {len(correlated)} events correlated with ACTofGOD events\n")
print("First 15 correlated events:\n")

for i, row in enumerate(correlated[:15], 1):
    print(f"{i}. {row['Event_Date']} | {row['CATEGORY']:10} | {row['SUBCATEGORY']:20} | {row['CORRELATION']}")
