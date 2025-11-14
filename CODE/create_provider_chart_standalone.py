# ◸──────── ✧ ──────── ◇ ———————🔹-💠-🔹——————— ◇ ──────── ✧ ────────◹
#       SECTION: Provider Breakdown Chart - Using Statistical Analysis Data
# ◺──────── ✧ ──────── ◇ ———————🔹-💠-🔹——————— ◇ ──────── ✧ ────────◿

import matplotlib.pyplot as plt
import numpy as np

# Set professional style
plt.style.use('seaborn-v0_8-darkgrid')

# Data from your statistical analysis (big three providers)
# Based on correlation report showing:
# - Anthropic: 53.7% correlation rate (175 total incidents)
# - OpenAI: 57.6% correlation rate (264 total incidents)
# - Google: 81.8% correlation rate (33 total incidents)

provider_data = {
    'Provider': ['Anthropic', 'OpenAI', 'Google'],
    'Total': [175, 264, 33],
    'Correlation_Rate': [53.7, 57.6, 81.8]
}

# Calculate correlated events
provider_data['Correlated'] = [
    int(provider_data['Total'][i] * provider_data['Correlation_Rate'][i] / 100)
    for i in range(len(provider_data['Provider']))
]

fig, ax = plt.subplots(figsize=(10, 7))

x = np.arange(len(provider_data['Provider']))
width = 0.35

bars1 = ax.bar(x - width/2, provider_data['Total'], width, label='Total Incidents',
               color='#3498DB', edgecolor='black', linewidth=1.5)
bars2 = ax.bar(x + width/2, provider_data['Correlated'], width,
               label='Within 72h of Space Weather',
               color='#E74C3C', edgecolor='black', linewidth=1.5)

# Add percentage labels on top
for i in range(len(provider_data['Provider'])):
    rate = provider_data['Correlation_Rate'][i]
    total = provider_data['Total'][i]
    ax.text(i, total + 10, f"{rate:.1f}%",
           ha='center', va='bottom', fontweight='bold', fontsize=12)

ax.set_ylabel('Number of Incidents', fontsize=13, fontweight='bold')
ax.set_xlabel('AI Provider', fontsize=13, fontweight='bold')
ax.set_title('AI System Failures by Provider: Space Weather Correlation\n(2025 Data)',
             fontsize=15, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(provider_data['Provider'], fontsize=12)
ax.legend(fontsize=11, loc='upper left')
ax.grid(True, alpha=0.3, axis='y')

# Add a note about the data
ax.text(0.98, 0.02, 'Data: 2025 LLM incidents (Jan-Nov)\nAnalysis: Permutation testing, p < 0.01',
        transform=ax.transAxes, fontsize=9, verticalalignment='bottom',
        horizontalalignment='right', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))

plt.tight_layout()

output_path = r'C:\Users\Merci\OneDrive\Desktop\2025\2025\csv\provider_breakdown.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"[SUCCESS] Provider breakdown chart created: {output_path}")
print(f"\nProvider Statistics:")
for i in range(len(provider_data['Provider'])):
    print(f"  {provider_data['Provider'][i]}: {provider_data['Total'][i]} total, "
          f"{provider_data['Correlated'][i]} correlated ({provider_data['Correlation_Rate'][i]:.1f}%)")

plt.close()
