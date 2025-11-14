# ◸──────── ✧ ──────── ◇ ———————🔹-💠-🔹——————— ◇ ──────── ✧ ────────◹
#       SECTION: Correlation Report - Statistical Analysis
# ◺──────── ✧ ──────── ◇ ———————🔹-💠-🔹——————— ◇ ──────── ✧ ────────◿

import csv
from collections import defaultdict

input_file = r'C:\Users\Merci\OneDrive\Desktop\2025\2025\csv\New_Master_with_correlations.csv'

# Read all data
rows = []
with open(input_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

# Categorize events
actofgod_events = [r for r in rows if r['CATEGORY'] == 'ACTofGOD']
llm_events = [r for r in rows if r['CATEGORY'] == 'LLM']
network_events = [r for r in rows if r['CATEGORY'] == 'NETWORK']
correlated_events = [r for r in rows if r.get('CORRELATION', '') and r['CORRELATION'] != 'SOURCE_EVENT']
llm_correlated = [r for r in correlated_events if r['CATEGORY'] == 'LLM']
network_correlated = [r for r in correlated_events if r['CATEGORY'] == 'NETWORK']

# Count by provider for LLM events
llm_by_provider = defaultdict(int)
llm_correlated_by_provider = defaultdict(int)

for event in llm_events:
    provider = event.get('SUBCATEGORY', 'Unknown')
    llm_by_provider[provider] += 1

for event in llm_correlated:
    provider = event.get('SUBCATEGORY', 'Unknown')
    llm_correlated_by_provider[provider] += 1

# Print report
print("=" * 80)
print("CORRELATION ANALYSIS REPORT")
print("ACTofGOD Events vs. Tech Incidents (72-hour window)")
print("=" * 80)

print(f"\n[OVERALL STATISTICS]")
print(f"Total events in dataset: {len(rows)}")
print(f"ACTofGOD events (solar/geomagnetic): {len(actofgod_events)}")
print(f"LLM incidents: {len(llm_events)}")
print(f"Network incidents: {len(network_events)}")
print(f"\nEvents occurring within 72h AFTER ACTofGOD: {len(correlated_events)}")
print(f"  - LLM incidents: {len(llm_correlated)} ({len(llm_correlated)/len(llm_events)*100:.1f}% of all LLM incidents)")
print(f"  - Network incidents: {len(network_correlated)} ({len(network_correlated)/len(network_events)*100 if len(network_events) > 0 else 0:.1f}% of all network incidents)")

print(f"\n[CORRELATION RATE]")
total_tech_events = len(llm_events) + len(network_events)
total_correlated_tech = len(llm_correlated) + len(network_correlated)
correlation_rate = (total_correlated_tech / total_tech_events * 100) if total_tech_events > 0 else 0
print(f"Percentage of tech incidents within 72h of ACTofGOD event: {correlation_rate:.1f}%")

print(f"\n[LLM PROVIDERS - Correlation Breakdown]")
print(f"{'Provider':<20} {'Total Incidents':<15} {'Correlated':<15} {'Rate':<10}")
print("-" * 60)

for provider in sorted(llm_by_provider.keys()):
    total = llm_by_provider[provider]
    corr = llm_correlated_by_provider.get(provider, 0)
    rate = (corr / total * 100) if total > 0 else 0
    print(f"{provider:<20} {total:<15} {corr:<15} {rate:.1f}%")

print(f"\n[ACTofGOD EVENT TYPES]")
actofgod_types = defaultdict(int)
for event in actofgod_events:
    subcat = event.get('SUBCATEGORY', 'Unknown')
    actofgod_types[subcat] += 1

print(f"{'Event Type':<35} {'Count':<10}")
print("-" * 45)
for event_type in sorted(actofgod_types.keys(), key=lambda x: actofgod_types[x], reverse=True)[:15]:
    count = actofgod_types[event_type]
    print(f"{event_type:<35} {count:<10}")

print("\n" + "=" * 80)
print("[INTERPRETATION]")
print(f"Out of {len(llm_events)} LLM incidents, {len(llm_correlated)} ({correlation_rate:.1f}%) occurred")
print(f"within 72 hours AFTER a solar/geomagnetic event.")
print(f"\nThis suggests {'a strong' if correlation_rate > 50 else 'a moderate' if correlation_rate > 30 else 'some'} correlation between")
print(f"geomagnetic activity and AI system disruptions.")
print("=" * 80)
