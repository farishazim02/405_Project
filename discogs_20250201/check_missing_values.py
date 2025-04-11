import pandas as pd

# List of CSV files to check (explicitly provided)
csv_files = [
    "releases_part_2.csv",
    "releases_part_3.csv",
    "releases_part_rel_chunk_1.csv",
    "releases_part_rel_chunk_4.csv",
    "releases_part_rel_chunk_5.csv",
    "releases_part_rel_chunk_6.csv"
]

print("📋 Checking specified CSV files for missing values...")

for file in csv_files:
    print(f"\n🗂️ File: {file}")
    try:
        df = pd.read_csv(file)
        print(f"✅ Loaded {len(df)} rows × {len(df.columns)} columns")
        print("🔍 Missing values per column:")
        print(df.isnull().sum())
    except Exception as e:
        print(f"❌ Failed to load {file}: {e}")
