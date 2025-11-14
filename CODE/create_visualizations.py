# ◸──────── ✧ ──────── ◇ ———————🔹-💠-🔹——————— ◇ ──────── ✧ ────────◹
#       SECTION: Visualization Generator - Space Weather & AI Incidents
# ◺──────── ✧ ──────── ◇ ———————🔹-💠-🔹——————— ◇ ──────── ✧ ────────◿

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import seaborn as sns
import numpy as np

# Set professional style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# ◸──────── ✧ ──────── ◇ ———————🔹-💠-🔹——————— ◇ ──────── ✧ ────────◹
#       SECTION: Load Data
# ◺──────── ✧ ──────── ◇ ———————🔹-💠-🔹——————— ◇ ──────── ✧ ────────◿

def load_and_prepare_data(file_path: str) -> pd.DataFrame:
    """Load CSV and prepare data for visualization."""
    df = pd.read_csv(file_path, encoding='utf-8', on_bad_lines='skip')

    # Convert date column
    date_col = 'Event_Date' if 'Event_Date' in df.columns else 'EVENT_DATE'
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')

    # Standardize column names
    df.columns = df.columns.str.upper()

    return df

# ◸──────── ✧ ──────── ◇ ———————🔹-💠-🔹——————— ◇ ──────── ✧ ────────◹
#       SECTION: Visualization 1 - Timeline with Event Overlay
# ◺──────── ✧ ──────── ◇ ———————🔹-💠-🔹——————— ◇ ──────── ✧ ────────◿

def create_timeline_chart(df: pd.DataFrame, output_path: str):
    """Create timeline showing ACTofGOD events and LLM incidents."""

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 10), sharex=True,
                                    gridspec_kw={'height_ratios': [2, 1]})

    date_col = 'EVENT_DATE' if 'EVENT_DATE' in df.columns else 'Event_Date'

    # Group by date and category
    df_daily = df.groupby([pd.Grouper(key=date_col, freq='D'), 'CATEGORY']).size().unstack(fill_value=0)

    # Top panel: LLM incidents
    if 'LLM' in df_daily.columns:
        ax1.fill_between(df_daily.index, df_daily['LLM'], alpha=0.7, color='#FF6B6B', label='LLM Incidents')
        ax1.plot(df_daily.index, df_daily['LLM'], color='#C92A2A', linewidth=2)

    # Mark ACTofGOD events
    actofgod_events = df[df['CATEGORY'] == 'ACTOFGOD']
    for _, event in actofgod_events.iterrows():
        ax1.axvline(x=event[date_col], color='#FFA500', alpha=0.6, linewidth=1.5, linestyle='--')

    ax1.set_ylabel('LLM Incidents per Day', fontsize=12, fontweight='bold')
    ax1.set_title('AI System Incidents Following Space Weather Events',
                  fontsize=16, fontweight='bold', pad=20)
    ax1.legend(loc='upper left', fontsize=10)
    ax1.grid(True, alpha=0.3)

    # Bottom panel: ACTofGOD events timeline
    actofgod_df = df[df['CATEGORY'] == 'ACTOFGOD'].copy()

    if not actofgod_df.empty:
        # Count events by date
        actofgod_daily = actofgod_df.groupby(pd.Grouper(key=date_col, freq='D')).size()

        # Create the zigzag line plot
        ax2.fill_between(actofgod_daily.index, actofgod_daily.values,
                         alpha=0.4, color='#FFA500', label='Space Weather Events')
        ax2.plot(actofgod_daily.index, actofgod_daily.values,
                color='#FF6600', linewidth=2, marker='o', markersize=4)

        # Mark different event types with different markers
        for event_type, color, marker in [
            ('Schumann', '#9B59B6', 's'),
            ('NASA', '#3498DB', '^'),
            ('Solar', '#E74C3C', 'D'),
            ('Geomagnetic', '#F39C12', 'v'),
            ('NOAA', '#1ABC9C', 'p')
        ]:
            type_events = actofgod_df[actofgod_df['SUBCATEGORY'].str.contains(event_type, case=False, na=False)]
            if not type_events.empty:
                ax2.scatter(type_events[date_col], [1] * len(type_events),
                           s=100, marker=marker, color=color, label=event_type,
                           edgecolor='black', linewidth=0.5, zorder=5)

    ax2.set_ylabel('Space Weather Events\nper Day', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Date', fontsize=12, fontweight='bold')
    ax2.set_ylim(0, max(5, actofgod_daily.max() + 1) if not actofgod_df.empty else 5)
    ax2.legend(title='Event Type', loc='upper left', fontsize=9, ncol=2)
    ax2.grid(True, alpha=0.3)

    # Format x-axis
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax2.xaxis.set_major_locator(mdates.MonthLocator())
    plt.xticks(rotation=45, ha='right')

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"[OK] Timeline chart saved: {output_path}")
    plt.close()

# ◸──────── ✧ ──────── ◇ ———————🔹-💠-🔹——————— ◇ ──────── ✧ ────────◹
#       SECTION: Visualization 2 - Incident Rate Ratio Comparison
# ◺──────── ✧ ──────── ◇ ———————🔹-💠-🔹——————— ◇ ──────── ✧ ────────◿

def create_irr_chart(output_path: str):
    """Create bar chart showing Incident Rate Ratios."""

    # Data from statistical analysis
    data = {
        'Event Type': ['Any EM\n(24h)', 'Solar\n(24h)', 'Geomagnetic\n(24h)',
                       'Any EM\n(72h)', 'Solar\n(72h)', 'Geomagnetic\n(72h)'],
        'IRR': [1.47, 1.50, 2.10, 1.61, 1.50, 1.87],
        'p_value': [0.0043, 0.0083, 0.0059, 0.0007, 0.0035, 0.0086]
    }

    df = pd.DataFrame(data)

    fig, ax = plt.subplots(figsize=(12, 7))

    # Create bars with color based on significance
    colors = ['#E74C3C' if p < 0.01 else '#F39C12' for p in df['p_value']]
    bars = ax.bar(df['Event Type'], df['IRR'], color=colors, edgecolor='black', linewidth=1.5)

    # Add baseline reference
    ax.axhline(y=1.0, color='black', linestyle='--', linewidth=2, label='Baseline (no effect)')

    # Add value labels on bars
    for i, (bar, irr, p) in enumerate(zip(bars, df['IRR'], df['p_value'])):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                f'{irr:.2f}x\np={p:.4f}',
                ha='center', va='bottom', fontweight='bold', fontsize=10)

    ax.set_ylabel('Incident Rate Ratio (IRR)', fontsize=14, fontweight='bold')
    ax.set_xlabel('Event Type & Time Window', fontsize=14, fontweight='bold')
    ax.set_title('Impact of Space Weather on AI System Failures\nIncident Rate Ratios',
                 fontsize=16, fontweight='bold', pad=20)

    # Add significance legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#E74C3C', label='p < 0.01 (Highly Significant)'),
        Patch(facecolor='#F39C12', label='p < 0.05 (Significant)'),
        ax.get_lines()[0]  # Baseline line
    ]
    ax.legend(handles=legend_elements, loc='upper left', fontsize=10)

    ax.set_ylim(0, 2.5)
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"[OK] IRR comparison chart saved: {output_path}")
    plt.close()

# ◸──────── ✧ ──────── ◇ ———————🔹-💠-🔹——————— ◇ ──────── ✧ ────────◹
#       SECTION: Visualization 3 - Lag Effect Heat Map
# ◺──────── ✧ ──────── ◇ ———————🔹-💠-🔹——————— ◇ ──────── ✧ ────────◿

def create_lag_heatmap(output_path: str):
    """Create heat map showing lag effect."""

    # Data from lag analysis
    data = {
        'Any EM': [2.42, 3.16, 3.09, 2.82],
        'Solar': [2.79, 3.25, 3.16, 3.13],
        'Geomagnetic': [3.71, 4.57, 4.57, 3.71],
        'Schumann': [1.56, 2.30, 2.67, 2.26],
        'Other': [2.30, 3.60, 3.60, 3.10]
    }

    df = pd.DataFrame(data, index=['Day 0\n(During)', 'Day 1\n(+24h)', 'Day 2\n(+48h)', 'Day 3\n(+72h)'])

    fig, ax = plt.subplots(figsize=(10, 6))

    # Create heatmap
    im = ax.imshow(df.values, cmap='YlOrRd', aspect='auto', vmin=0, vmax=5)

    # Set ticks
    ax.set_xticks(np.arange(len(df.columns)))
    ax.set_yticks(np.arange(len(df.index)))
    ax.set_xticklabels(df.columns)
    ax.set_yticklabels(df.index)

    # Add colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Mean LLM Incidents per Day', rotation=270, labelpad=20, fontweight='bold')

    # Add text annotations
    for i in range(len(df.index)):
        for j in range(len(df.columns)):
            text = ax.text(j, i, f'{df.values[i, j]:.2f}',
                          ha="center", va="center", color="black", fontweight='bold', fontsize=11)

    ax.set_title('Lag Effect: AI Incidents Peak 24-48 Hours After Space Weather Events',
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel('Event Type', fontsize=12, fontweight='bold')
    ax.set_ylabel('Time After Event', fontsize=12, fontweight='bold')

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"[OK] Lag effect heatmap saved: {output_path}")
    plt.close()

# ◸──────── ✧ ──────── ◇ ———————🔹-💠-🔹——————— ◇ ──────── ✧ ────────◹
#       SECTION: Visualization 4 - Provider Breakdown
# ◺──────── ✧ ──────── ◇ ———————🔹-💠-🔹——————— ◇ ──────── ✧ ────────◿

def create_provider_chart(df: pd.DataFrame, output_path: str):
    """Create chart showing correlation by provider - focused on big three."""

    # Filter LLM events
    llm_df = df[df['CATEGORY'] == 'LLM'].copy()

    # Count total and correlated by provider (only the big three)
    provider_stats = []

    for provider in ['Anthropic', 'OpenAI', 'Google']:
        provider_events = llm_df[llm_df['SUBCATEGORY'].str.contains(provider, case=False, na=False)]
        total = len(provider_events)

        # Count correlated events
        if 'CORRELATION' in df.columns:
            correlated = len(provider_events[
                (provider_events['CORRELATION'].notna()) &
                (provider_events['CORRELATION'].str.len() > 0) &
                (provider_events['CORRELATION'] != 'SOURCE_EVENT')
            ])
        else:
            correlated = 0

        if total > 0:
            rate = (correlated / total) * 100
            provider_stats.append({
                'Provider': provider,
                'Total': total,
                'Correlated': correlated,
                'Rate': rate
            })
            print(f"  {provider}: {total} total, {correlated} correlated ({rate:.1f}%)")

    if not provider_stats:
        print("[WARNING] No provider data available for chart")
        return

    df_providers = pd.DataFrame(provider_stats)

    fig, ax = plt.subplots(figsize=(10, 7))

    x = np.arange(len(df_providers))
    width = 0.35

    bars1 = ax.bar(x - width/2, df_providers['Total'], width, label='Total Incidents',
                   color='#3498DB', edgecolor='black', linewidth=1)
    bars2 = ax.bar(x + width/2, df_providers['Correlated'], width, label='After Space Weather',
                   color='#E74C3C', edgecolor='black', linewidth=1)

    # Add percentage labels
    for i, row in df_providers.iterrows():
        ax.text(i, row['Total'] + 5, f"{row['Rate']:.1f}%",
               ha='center', va='bottom', fontweight='bold', fontsize=11)

    ax.set_ylabel('Number of Incidents', fontsize=12, fontweight='bold')
    ax.set_xlabel('AI Provider', fontsize=12, fontweight='bold')
    ax.set_title('AI System Failures by Provider: Space Weather Correlation',
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(df_providers['Provider'])
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"[OK] Provider comparison chart saved: {output_path}")
    plt.close()

# ◸──────── ✧ ──────── ◇ ———————🔹-💠-🔹——————— ◇ ──────── ✧ ────────◹
#       SECTION: Main Execution
# ◺──────── ✧ ──────── ◇ ———————🔹-💠-🔹——————— ◇ ──────── ✧ ────────◿

if __name__ == '__main__':
    print("=" * 80)
    print("GENERATING VISUALIZATIONS: Space Weather & AI Correlation Study")
    print("=" * 80)

    # File paths
    input_file = r'C:\Users\Merci\OneDrive\Desktop\2025\2025\csv\NEWESTMASTER_W_CORR.csv'
    output_dir = r'C:\Users\Merci\OneDrive\Desktop\2025\2025\csv'

    try:
        # Load data
        print("\n[1/4] Loading data...")
        df = load_and_prepare_data(input_file)
        print(f"      Loaded {len(df)} events")

        # Generate visualizations
        print("\n[2/4] Creating timeline chart...")
        create_timeline_chart(df, f"{output_dir}\\timeline_chart.png")

        print("\n[3/4] Creating IRR comparison chart...")
        create_irr_chart(f"{output_dir}\\irr_comparison.png")

        print("\n[4/4] Creating lag effect heatmap...")
        create_lag_heatmap(f"{output_dir}\\lag_heatmap.png")

        print("\n[5/5] Creating provider breakdown chart...")
        create_provider_chart(df, f"{output_dir}\\provider_breakdown.png")

        print("\n" + "=" * 80)
        print("[SUCCESS] All visualizations generated!")
        print("=" * 80)
        print(f"\nFiles saved to: {output_dir}")
        print("  - timeline_chart.png")
        print("  - irr_comparison.png")
        print("  - lag_heatmap.png")
        print("  - provider_breakdown.png")
        print("\nReady for your presentation!")

    except Exception as e:
        print(f"\n[ERROR] Failed to generate visualizations: {e}")
        import traceback
        traceback.print_exc()
