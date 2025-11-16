#!/usr/bin/env python3
"""
Data Cleaning Module

Contains functions for cleaning and preprocessing student dataset.
"""

import pandas as pd
import numpy as np
from pathlib import Path

class DataCleaner:
    def __init__(self, csv_path: str):
        """Initialize DataCleaner with path to CSV."""
        self.csv_path = csv_path
        self.df = pd.read_csv(csv_path)

    def remove_duplicates(self):
        """Remove duplicate rows if any."""
        self.df.drop_duplicates(inplace=True)
        return self.df

    def handle_missing_values(self):
        """Placeholder: handle NaNs, fill or drop."""
        # TODO: implement missing value handling
        return self.df

    def correct_anomalies(self):
        """Placeholder: fix outliers or inconsistent values."""
        # TODO: implement anomaly correction logic
        return self.df

    def save_cleaned_data(self, output_path: str):
        """Save cleaned dataset to CSV."""
        self.df.to_csv(output_path, index=False)
        print(f"Cleaned data saved to {output_path}")
        return self.df

# -----------------------------
# Main execution
# -----------------------------
def main():
    BASE_DIR = Path(__file__).resolve().parent.parent
    DATA_CSV = BASE_DIR / "data" / "raw_students.csv"
    CLEANED_CSV = BASE_DIR / "data" / "students_cleaned.csv"

    cleaner = DataCleaner(csv_path=DATA_CSV)
    cleaner.remove_duplicates()
    cleaner.handle_missing_values()
    cleaner.correct_anomalies()
    cleaner.save_cleaned_data(CLEANED_CSV)

if __name__ == "__main__":
    main()
