import pandas as pd

df = pd.read_csv(r"C:\Users\darby\OneDrive\Desktop\medicaid-provider-spending.csv", nrows=100000)

print("Shape:", df.shape)
print("\nColumns:", df.columns.tolist())
print("\nFirst few rows:")
print(df.head())
print("\nData types:")
print(df.dtypes)
# Check for nulls
print("Null values:")
print(df.isnull().sum())

# Basic stats on the numeric columns
print("\nBasic statistics:")
print(df[['TOTAL_UNIQUE_BENEFICIARIES', 'TOTAL_CLAIMS', 'TOTAL_PAID']].describe())
# Calculate spend per beneficiary
df['SPEND_PER_BENEFICIARY'] = df['TOTAL_PAID'] / df['TOTAL_UNIQUE_BENEFICIARIES']

print("Spend per beneficiary stats:")
print(df['SPEND_PER_BENEFICIARY'].describe())
# Find the highest spend per beneficiary
top_outliers = df.nlargest(10, 'SPEND_PER_BENEFICIARY')[
    ['BILLING_PROVIDER_NPI_NUM', 'HCPCS_CODE',
     'CLAIM_FROM_MONTH', 'TOTAL_UNIQUE_BENEFICIARIES',
     'TOTAL_PAID', 'SPEND_PER_BENEFICIARY']
]

print("Top 10 highest spend per beneficiary:")
print(top_outliers.to_string())
# Look at S9124 specifically
s9124 = df[df['HCPCS_CODE'] == 'S9124']
print(s9124[['BILLING_PROVIDER_NPI_NUM', 'CLAIM_FROM_MONTH',
             'TOTAL_UNIQUE_BENEFICIARIES', 'TOTAL_PAID',
             'SPEND_PER_BENEFICIARY']])
# Flag the S9124 outlier
top_s9124 = df[df['HCPCS_CODE'] == 'S9124'].nlargest(5, 'SPEND_PER_BENEFICIARY')
print("Top S9124 outliers:")
print(top_s9124[['BILLING_PROVIDER_NPI_NUM', 'CLAIM_FROM_MONTH',
                  'TOTAL_UNIQUE_BENEFICIARIES', 'TOTAL_PAID',
                  'SPEND_PER_BENEFICIARY']].to_string())
# How many months does this provider appear?
provider_history = df[df['BILLING_PROVIDER_NPI_NUM'] == '1528351285']
print("Provider 1528351285 full history in this sample:")
print(provider_history[['HCPCS_CODE', 'CLAIM_FROM_MONTH',
                         'TOTAL_UNIQUE_BENEFICIARIES',
                         'TOTAL_PAID']].to_string())
# Total billing for this provider
total = provider_history['TOTAL_PAID'].sum()
print(f"Total paid to provider 1528351285: ${total:,.2f}")
print(f"Number of months appearing: {len(provider_history)}")
print(f"HCPCS codes used: {provider_history['HCPCS_CODE'].unique()}")
# Document fraud flag #1
print("=" * 60)
print("FRAUD FLAG #1: Quality One Care Home Health Inc.")
print("NPI: 1528351285")
print("Location: Silver Spring, MD")
print(f"Total Medicaid paid (sample): ${total:,.2f}")
print("Months active in sample: 37")
print("HCPCS codes: T1003 (LPN 15-min), S9124 (LPN hourly)")
print("Flag: Mathematically impossible LPN hours per beneficiary")
print("=" * 60)
# Reusable outlier detection function
def flag_outliers(df, code, threshold_multiplier=3):
    subset = df[df['HCPCS_CODE'] == code].copy()
    if subset.empty:
        return None
    mean = subset['SPEND_PER_BENEFICIARY'].mean()
    std = subset['SPEND_PER_BENEFICIARY'].std()
    threshold = mean + (threshold_multiplier * std)
    outliers = subset[subset['SPEND_PER_BENEFICIARY'] > threshold]
    outliers = outliers.sort_values('SPEND_PER_BENEFICIARY', ascending=False)
    return outliers[['BILLING_PROVIDER_NPI_NUM', 'HCPCS_CODE',
                      'CLAIM_FROM_MONTH', 'TOTAL_UNIQUE_BENEFICIARIES',
                      'TOTAL_PAID', 'SPEND_PER_BENEFICIARY']]

# Run it on T1003
print("Statistical outliers for T1003:")
t1003_flags = flag_outliers(df, 'T1003')
print(t1003_flags.to_string())
print(f"\nTotal flagged: {len(t1003_flags)}")
# Investigate second flagged provider
provider2 = df[df['BILLING_PROVIDER_NPI_NUM'] == '1225205354']
total2 = provider2['TOTAL_PAID'].sum()
print(f"Total paid to provider 1225205354: ${total2:,.2f}")
print(f"Months appearing: {len(provider2)}")
print(f"HCPCS codes: {provider2['HCPCS_CODE'].unique()}")
print(provider2[['HCPCS_CODE', 'CLAIM_FROM_MONTH',
                  'TOTAL_UNIQUE_BENEFICIARIES', 'TOTAL_PAID']].to_string())
total2 = provider2['TOTAL_PAID'].sum()
print(f"Total paid to NPI 1225205354: ${total2:,.2f}")
print(f"Months in sample: {len(provider2)}")
print("=" * 60)
print("FRAUD FLAG #2: Greater New York Home Care LLC")
print("AKA: Greater New York Nursing Services")
print("NPI: 1225205354")
print("Location: Brooklyn, NY")
print(f"Total Medicaid paid (sample): ${total2:,.2f}")
print("Months active in sample: 74")
print("HCPCS codes: T1003 (LPN 15-min), S9124 (LPN hourly)")
print("Flag: Sustained high-volume LPN billing 2019-2024")
print("Flag: Same billing pattern as NPI 1528351285 (MD)")
print("Flag: Mathematically impossible LPN hours per beneficiary")
print("=" * 60)
# Get every unique HCPCS code in the dataset
all_codes = df['HCPCS_CODE'].unique()
print(f"Total unique HCPCS codes: {len(all_codes)}")

# Collect all flagged rows into a list, then combine
all_flags = []

for code in all_codes:
    result = flag_outliers(df, code)
    if result is not None and not result.empty:
        all_flags.append(result)

# Combine into one master dataframe
if all_flags:
    master_flags = pd.concat(all_flags, ignore_index=True)
    master_flags = master_flags.sort_values('SPEND_PER_BENEFICIARY', ascending=False)
    print(f"\nTotal flagged records: {len(master_flags)}")
    print(f"Unique flagged providers: {master_flags['BILLING_PROVIDER_NPI_NUM'].nunique()}")
    print(master_flags.head(20).to_string())
else:
    print("No outliers found.")
# ── PHASE 2: GroupBy Aggregation ──────────────────────────────────────────────

# Summarize each flagged provider across all their flagged records
provider_summary = master_flags.groupby('BILLING_PROVIDER_NPI_NUM').agg(
    total_paid        = ('TOTAL_PAID', 'sum'),
    flagged_months    = ('CLAIM_FROM_MONTH', 'count'),
    unique_codes      = ('HCPCS_CODE', 'nunique'),
    avg_spend_per_ben = ('SPEND_PER_BENEFICIARY', 'mean'),
    max_spend_per_ben = ('SPEND_PER_BENEFICIARY', 'max'),
    codes_used        = ('HCPCS_CODE', lambda x: ', '.join(x.unique()))
).reset_index()

# Sort by total dollars flagged
provider_summary = provider_summary.sort_values('total_paid', ascending=False)

print(f"Flagged provider summary (top 20):")
print(provider_summary.head(20).to_string())
# ── RISK SCORING ──────────────────────────────────────────────────────────────

# Normalize each component to a 0-1 scale, then weight them
# We're creating a composite fraud risk score from three signals:
#   1. Total dollars (raw financial exposure)
#   2. Flagged months (persistence — longer pattern = more concerning)
#   3. Avg spend per beneficiary (intensity per patient)

from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()

# Select the columns we want to normalize
score_inputs = provider_summary[['total_paid', 'flagged_months', 'avg_spend_per_ben']].copy()

# Normalize each to 0-1
normalized = scaler.fit_transform(score_inputs)

# Apply weights — adjust these based on what you consider most important
weight_total_paid    = 0.40
weight_months        = 0.35
weight_avg_spend     = 0.25

provider_summary['risk_score'] = (
    normalized[:, 0] * weight_total_paid +
    normalized[:, 1] * weight_months +
    normalized[:, 2] * weight_avg_spend
)

# Scale to 0-100 for readability
provider_summary['risk_score'] = (provider_summary['risk_score'] * 100).round(1)

# Re-sort by risk score
provider_summary = provider_summary.sort_values('risk_score', ascending=False)

print("Top 20 providers by fraud risk score:")
print(provider_summary[['BILLING_PROVIDER_NPI_NUM', 'total_paid',
                         'flagged_months', 'avg_spend_per_ben',
                         'risk_score', 'codes_used']].head(20).to_string())
# ── FLAG HIGH RISK AND EXPORT ─────────────────────────────────────────────────

# Binary flag for Tableau filtering
provider_summary['high_risk'] = provider_summary['risk_score'] >= 50

print(f"\nHigh risk providers (score >= 50): {provider_summary['high_risk'].sum()}")
print(f"Lower risk flagged providers: {(~provider_summary['high_risk']).sum()}")

# Export master flags (every flagged record)
master_flags.to_csv(r'C:\Users\darby\OneDrive\Desktop\phase1_flagged_records.csv', index=False)

# Export provider summary with risk scores
provider_summary.to_csv(r'C:\Users\darby\OneDrive\Desktop\phase1_provider_summary.csv', index=False)

print("\nExported:")
print("  phase1_flagged_records.csv   — all 1,109 flagged records")
print("  phase1_provider_summary.csv  — 194 providers with risk scores")
