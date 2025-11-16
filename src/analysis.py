#!/usr/bin/env python3
"""
Analysis Module

Contains functions to compute statistics and basic analysis on student dataset.
"""

import pandas as pd
import numpy as np
from pathlib import Path

class DataAnalyzer:
    def __init__(self, csv_path: str):
        """Initialize DataAnalyzer with path to CSV."""
        self.csv_path = csv_path
        self.df = pd.read_csv(csv_path)

    def summary_statistics(self):
        """Placeholder: generate summary statistics (mean, median, std)."""
        # TODO: implement summary statistics
        return self.df.describe()

    def correlation_matrix(self):
        """Placeholder: compute correlations between numeric columns."""
        # TODO: implement correlation calculation
        return self.df.corr()

    def group_analysis(self):
        """Placeholder: group data by categories (e.g., gender) and aggregate."""
        # TODO: implement group-wise analysis
        return None

# -----------------------------
# Main execution
# -----------------------------
def main():
    BASE_DIR = Path(__file__).resolve().parent.parent
    CLEANED_CSV = BASE_DIR / "data" / "students_cleaned.csv"

    analyzer = DataAnalyzer(csv_path=CLEANED_CSV)
    print(analyzer.summary_statistics())
    print(analyzer.correlation_matrix())
    # analyzer.group_analysis() # TODO

if __name__ == "__main__":
    main()
