#!/usr/bin/env python3
"""
Visualization Module

Contains functions to visualize student dataset.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

class DataVisualizer:
    def __init__(self, csv_path: str):
        """Initialize DataVisualizer with path to CSV."""
        self.csv_path = csv_path
        self.df = pd.read_csv(csv_path)

    def histogram_age(self):
        """Placeholder: plot histogram of student ages."""
        # TODO: implement
        pass

    def scatter_study_vs_performance(self):
        """Placeholder: plot scatter of study hours vs past performance."""
        # TODO: implement
        pass

    def boxplot_quiz_participation(self):
        """Placeholder: plot boxplot of quiz participation."""
        # TODO: implement
        pass

# -----------------------------
# Main execution
# -----------------------------
def main():
    BASE_DIR = Path(__file__).resolve().parent.parent
    CLEANED_CSV = BASE_DIR / "data" / "students_cleaned.csv"

    viz = DataVisualizer(csv_path=CLEANED_CSV)
    # viz.histogram_age()
    # viz.scatter_study_vs_performance()
    # viz.boxplot_quiz_participation()

if __name__ == "__main__":
    main()
