#!/usr/bin/env python3
"""
Data Diagnosis Helper

Use this script to quickly inspect a student dataset
- types, missing values, unique counts, basic stats
- boolean columns summary
- outlier check for numeric columns
"""

from pathlib import Path
import pandas as pd
import numpy as np

# -----------------------------
# 1. Paths
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# -----------------------------
# 2. Select file to analyze
# -----------------------------
# Uncomment the file you want to check:

#csv_file = DATA_DIR / "students_raw.csv"
csv_file = DATA_DIR / "students_cleaned.csv"  # example for cleaned dataset

# -----------------------------
# 3. Load dataset
# -----------------------------
df = pd.read_csv(csv_file)

# -----------------------------
# 4. Basic info
# -----------------------------
print("\n=== Dataset Info ===")
df.info()

print("\n=== Column Data Types ===")
print(df.dtypes)

print("\n=== First 5 Rows ===")
print(df.head())

print("\n=== Missing Values ===")
print(df.isna().sum())

print("\n=== Missing Values Percentage ===")
print((df.isna().sum() / len(df) * 100).round(2))

# -----------------------------
# 5. Numeric summary
# -----------------------------
print("\n=== Numeric Columns Summary ===")
print(df.describe())

# -----------------------------
# 6. Unique counts
# -----------------------------
print("\n=== Unique Values per Column ===")
print(df.nunique())

# -----------------------------
# 7. Boolean columns summary
# -----------------------------
bool_cols = df.select_dtypes(include=['bool', 'boolean']).columns
if len(bool_cols) > 0:
    print("\n=== Boolean Columns Value Counts ===")
    for col in bool_cols:
        print(f"\nColumn: {col}")
        print(df[col].value_counts(dropna=False))

# -----------------------------
# 8. Quick outlier detection for numeric columns
# -----------------------------
numeric_cols = df.select_dtypes(include=[np.number]).columns
print("\n=== Numeric Columns Outliers (below Q1-1.5*IQR or above Q3+1.5*IQR) ===")
for col in numeric_cols:
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    outliers = df[(df[col] < lower) | (df[col] > upper)]
    print(f"{col}: {len(outliers)} outliers ({(len(outliers)/len(df)*100):.2f}%)")

# -----------------------------
# 9. Quiz Participation Analysis
# -----------------------------
def diagnose_quiz_participation(df: pd.DataFrame):
    """
    Check for non-numeric / inconsistent values in 'quiz_participation'.
    Prints counts and examples.
    """
    col = 'quiz_participation'
    
    if col not in df.columns:
        print(f"\n=== Quiz Participation Analysis ===")
        print(f"Warning: Column '{col}' not found in the dataset.")
        return
        
    # Convert all values to string for consistent processing
    all_values = df[col].astype(str)
    
    # Check which values can't be converted to float
    def is_number(x):
        try:
            float(x)
            return True
        except ValueError:
            return False

    non_numeric_mask = ~all_values.apply(is_number)
    non_numeric_count = non_numeric_mask.sum()
    
    print(f"\n=== Quiz Participation Analysis ===")
    print(f"Total rows: {len(df)}")
    print(f"Non-numeric '{col}' values: {non_numeric_count} ({(non_numeric_count/len(df)*100):.1f}%)")
    
    if non_numeric_count > 0:
        print("\nExamples of non-numeric/inconsistent values:")
        print(all_values[non_numeric_mask].unique()[:10])
    else:
        print("All values are numeric.")
    
    # Additional stats for numeric values
    numeric_mask = all_values.apply(is_number)
    if numeric_mask.any():
        print("\nNumeric values summary:")
        numeric_series = pd.to_numeric(all_values[numeric_mask], errors='coerce')
        print(f"  Min: {numeric_series.min():.2f}")
        print(f"  Max: {numeric_series.max():.2f}")
        print(f"  Mean: {numeric_series.mean():.2f}")
        print(f"  Median: {numeric_series.median():.2f}")

# Run the diagnosis
diagnose_quiz_participation(df)
# -----------------------------
# Quiz Participation Analysis Comment
# -----------------------------
# Checked 'quiz_participation' column after introducing inconsistencies:
# - Total rows: 500
# - Non-numeric values: 0
# Conclusion:
#   * All values are numeric (float), even after introducing small anomalies.
#   * Outliers or inconsistent formats (like fractions) are rare and will be handled by clipping later.
#   * No further cleaning or conversion is required for this column.

# -----------------------------
# 10. Optional: save a small report
# -----------------------------
# report_file = DATA_DIR / "data_diagnosis_report.txt"
# with open(report_file, 'w') as f:
#     f.write("=== Dataset Info ===\n")
#     df.info(buf=f)
#     f.write("\n\n=== Missing Values ===\n")
#     f.write(str(df.isna().sum()))
#     f.write("\n\n=== Numeric Summary ===\n")
#     f.write(str(df.describe()))
# print(f"\nReport saved to: {report_file}")
