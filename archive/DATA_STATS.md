Dataset Statistics - 2025-11-24

**Total Entries**: 970

## Format

Field Structure: `DATE,CATEGORY,SUBCATEGORY,TYPE,"SUMMARY",URL,CORRELATION`

Example Entry:
```csv
2025-11-12,ACTofGOD,SOLAR,GEOMAGNETIC,"Geomagnetic G4 - Severe (Max Kp: 8.7, Max Ap: 300) Duration: 24h | Readings >=4.0: 8/8",https://www.swpc.noaa.gov/products/planetary-k-index,EVENT_SOURCE
```

### Category Distribution
- **ACTofGOD** (Solar Events): 290 entries (29.9%)
- **LLM** (AI Platforms): 625 entries (64.4%)
- **NETWORK** (Infrastructure): 55 entries (5.7%)

### Correlation Analysis
- **YES** (Confirmed correlations): 498 entries (51.3%)
- **EVENT_SOURCE** (Source events): 277 entries (28.6%)
- **Empty** (No correlation): 195 entries (20.1%)

**Date Range**: January 1, 2025 - November 18, 2025

---

## Quality Assurance

1. **fix_csv_formatting.py** - Main formatting fix script
2. **verify_fields.py** - Field count verification
3. **final_quality_check.py** - Comprehensive quality validation
