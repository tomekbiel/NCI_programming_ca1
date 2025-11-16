#!/usr/bin/env python3
"""
Analysis Module
================

This module performs descriptive analysis of the cleaned student dataset.
It contains all mandatory elements required by the assignment and additional
extended analytical components inspired by standard academic methodology
(skewness, kurtosis, distribution diagnostics, contingency tables).

---------------------------------------------------------------------
MANDATORY ELEMENTS (REQUIRED)
---------------------------------------------------------------------
1. summary_statistics()        – mean, median, std for key numeric vars
2. correlation_matrix()        – correlations between numerical variables
3. group_analysis()            – group-by summary (completion vs engagement)
4. filter_high_engagement()    – filtering example
5. classify_performance()      – apply + lambda transformation

---------------------------------------------------------------------
EXTENDED ANALYSIS (MINCLUDED BY DEFAULT)
---------------------------------------------------------------------
6. distribution_shape()        – skewness, kurtosis, IQR; distribution profile
7. outlier_detection()         – 2×IQR rule
8. distribution_check_pdf()    – empirical vs theoretical PDF comparison
9. contingency_tables()        – multidimensional categorical analysis
                                similar to "Titanic" example in R textbooks
"""

import pandas as pd
import numpy as np
from pathlib import Path
from scipy.stats import norm


class DataAnalyzer:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.df = pd.read_csv(csv_path)

    # ================================================================
    # 1. MANDATORY — Descriptive statistics
    # ================================================================
    def summary_statistics(self):
        """Return mean, median and standard deviation for required variables."""
        stats = {
            "study_hours_mean": self.df["study_hours"].mean(),
            "study_hours_median": self.df["study_hours"].median(),
            "study_hours_std": self.df["study_hours"].std(),

            "quiz_part_mean": self.df["quiz_participation"].mean(),
            "quiz_part_median": self.df["quiz_participation"].median(),
            "quiz_part_std": self.df["quiz_participation"].std(),
        }
        return pd.Series(stats)

    # ================================================================
    # 2. MANDATORY — Correlation matrix
    # ================================================================
    def correlation_matrix(self):
        numeric_df = self.df.select_dtypes(include=[np.number])
        return numeric_df.corr()

    # ================================================================
    # 3. MANDATORY — Grouped analysis
    # ================================================================
    def group_analysis(self):
        """Group by course_completion (mandatory) and compute avg engagement."""
        return self.df.groupby("course_completion")["engagement"].mean()

    # ================================================================
    # 4. MANDATORY — Filtering example
    # ================================================================
    def filter_high_engagement(self, threshold=0.8):
        """Filter students with engagement above threshold."""
        return self.df[self.df["engagement"] > threshold]

    # ================================================================
    # 5. MANDATORY — apply + lambda classification
    # ================================================================
    def classify_performance(self):
        """Classify past performance into High/Medium/Low."""
        def classify(score):
            if score >= 85:
                return "High"
            elif score >= 60:
                return "Medium"
            return "Low"

        self.df["performance_level"] = self.df["past_performance"].apply(classify)
        return self.df[["past_performance", "performance_level"]]

    # ================================================================
    # 6. EXTENDED — Distribution shape (skewness, kurtosis, IQR)
    # ================================================================
    def distribution_shape(self, column="study_hours"):
        """Extended descriptive statistics for academic analysis."""
        data = self.df[column]
        return pd.Series({
            "mean": data.mean(),
            "median": data.median(),
            "std": data.std(),
            "skewness": data.skew(),
            "kurtosis": data.kurtosis(),
            "iqr": data.quantile(0.75) - data.quantile(0.25),
        })

    # ================================================================
    # 7. EXTENDED — Outlier detection (2×IQR rule)
    # ================================================================
    def outlier_detection(self, column="study_hours", multiplier=2.0):
        data = self.df[column]
        q1, q3 = data.quantile([0.25, 0.75])
        iqr = q3 - q1
        lower = q1 - multiplier * iqr
        upper = q3 + multiplier * iqr
        mask = (data < lower) | (data > upper)
        return {
            "lower_bound": lower,
            "upper_bound": upper,
            "n_outliers": int(mask.sum())
        }

    # ================================================================
    # 8. EXTENDED — Empirical vs theoretical PDF (normal)
    # ================================================================
    def distribution_check_pdf(self, column="study_hours"):
        """Compare empirical z-scores with normal PDF values (non-test)."""
        data = self.df[column].dropna()
        z = (data - data.mean()) / data.std()
        pdf_vals = norm.pdf(z)
        return pd.DataFrame({
            "z_score": z.head(10).values,
            "normal_pdf": pdf_vals[:10]
        })

    # ================================================================
    # 9. EXTENDED — Contingency tables (categorical cross-analysis)
    # ================================================================
    def contingency_tables(self):
        """Produce cross-tabulations for categorical variables."""
        tables = {}

        # Correct variable names based on CSV
        if "gender" in self.df.columns and "course_completion" in self.df.columns:
            tables["gender_course_completion"] = pd.crosstab(
                self.df["gender"], self.df["course_completion"], margins=True
            )

        if "age_bucket" in self.df.columns and "course_completion" in self.df.columns:
            tables["age_course_completion"] = pd.crosstab(
                self.df["age_bucket"], self.df["course_completion"], margins=True
            )

        if "performance_level" in self.df.columns and "course_completion" in self.df.columns:
            tables["performance_course_completion"] = pd.crosstab(
                self.df["performance_level"], self.df["course_completion"], margins=True
            )

        return tables


# ================================================================
# Main execution (local testing only)
# ================================================================
def main():
    BASE_DIR = Path(__file__).resolve().parent.parent
    CLEANED_CSV = BASE_DIR / "data" / "students_cleaned.csv"

    analyzer = DataAnalyzer(csv_path=CLEANED_CSV)

    print("\n=== Summary Statistics ===")
    print(analyzer.summary_statistics())

    print("\n=== Correlation Matrix ===")
    print(analyzer.correlation_matrix())

    print("\n=== Grouped Analysis (Course Completion vs Engagement) ===")
    print(analyzer.group_analysis())

    print("\n=== Distribution Shape (study_hours) ===")
    print(analyzer.distribution_shape())

    print("\n=== Outliers (2×IQR) ===")
    print(analyzer.outlier_detection())

    print("\n=== Example Contingency Tables ===")
    print(analyzer.contingency_tables())


if __name__ == "__main__":
    main()
