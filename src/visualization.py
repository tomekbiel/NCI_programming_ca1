#!/usr/bin/env python3
"""
Data Visualisation Module

Generates required and extended visualisations for the cleaned student dataset.

Mandatory:
1. Scatter plot: study_hours vs past_performance, colour by course_completion
2. Histogram: quiz_participation
3. Bar chart: average engagement by course_completion

Extended (magister-level):
4. Boxplots with outliers for numeric columns
5. Histograms with mean, median, skewness, kurtosis
6. Barplots for contingency tables (categorical cross-analysis)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

class DataVisualizer:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.df = pd.read_csv(csv_path)

    # ================================================================
    # 1. Scatter plot: study_hours vs past_performance
    # ================================================================
    def scatter_study_vs_performance(self):
        plt.figure(figsize=(8,6))
        sns.scatterplot(
            data=self.df,
            x="study_hours",
            y="past_performance",
            hue="course_completion",
            style="course_completion",
            palette="Set1",
            s=60
        )
        plt.title("Study Hours vs Past Performance")
        plt.xlabel("Study Hours")
        plt.ylabel("Past Performance (%)")
        plt.legend(title="Course Completed")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    # ================================================================
    # 2. Histogram: quiz_participation
    # ================================================================
    def histogram_quiz_participation(self):
        plt.figure(figsize=(8,6))
        sns.histplot(self.df["quiz_participation"], bins=20, kde=True, color="skyblue")
        plt.title("Distribution of Quiz Participation")
        plt.xlabel("Quiz Participation (%)")
        plt.ylabel("Count")
        plt.grid(axis="y")
        plt.tight_layout()
        plt.show()

    # ================================================================
    # 3. Bar chart: average engagement by course_completion
    # ================================================================
    def bar_engagement_by_completion(self):
        plt.figure(figsize=(6,5))
        mean_engagement = self.df.groupby("course_completion")["engagement"].mean().reset_index()
        sns.barplot(
            data=mean_engagement,
            x="course_completion",
            y="engagement",
            palette="pastel"
        )
        plt.title("Average Engagement by Course Completion")
        plt.xlabel("Course Completed")
        plt.ylabel("Average Engagement")
        plt.ylim(0,1)
        plt.tight_layout()
        plt.show()

    # ================================================================
    # 4. Boxplots with outliers for numeric variables
    # ================================================================
    def boxplots_numeric(self):
        numeric_cols = ["study_hours", "quiz_participation", "past_performance", "engagement"]
        plt.figure(figsize=(10,6))
        sns.boxplot(data=self.df[numeric_cols], palette="Set3")
        plt.title("Boxplots of Numeric Variables (outliers included)")
        plt.ylabel("Values")
        plt.xticks(rotation=15)
        plt.tight_layout()
        plt.show()

    # ================================================================
    # 5. Histograms with mean, median, skewness, kurtosis
    # ================================================================
    def histograms_distribution_stats(self):
        numeric_cols = ["study_hours", "quiz_participation", "past_performance", "engagement"]
        for col in numeric_cols:
            plt.figure(figsize=(8,5))
            sns.histplot(self.df[col], bins=20, kde=True, color="lightgreen")
            mean = self.df[col].mean()
            median = self.df[col].median()
            skew = self.df[col].skew()
            kurt = self.df[col].kurtosis()
            plt.axvline(mean, color='red', linestyle='--', label=f"Mean={mean:.2f}")
            plt.axvline(median, color='blue', linestyle='-', label=f"Median={median:.2f}")
            plt.title(f"{col} distribution (skew={skew:.2f}, kurtosis={kurt:.2f})")
            plt.xlabel(col)
            plt.ylabel("Count")
            plt.legend()
            plt.tight_layout()
            plt.show()

    # ================================================================
    # 6. Barplots for contingency tables (categorical variables)
    # ================================================================
    def barplots_contingency_tables(self):
        # gender × course_completion
        if "gender" in self.df.columns:
            ct_gender = pd.crosstab(self.df["gender"], self.df["course_completion"])
            ct_gender.plot(kind="bar", stacked=True, figsize=(6,5), colormap="Set2")
            plt.title("Gender vs Course Completion")
            plt.xlabel("Gender")
            plt.ylabel("Count")
            plt.legend(title="Course Completed")
            plt.tight_layout()
            plt.show()

        # age_bucket × course_completion
        if "age_bucket" in self.df.columns:
            ct_age = pd.crosstab(self.df["age_bucket"], self.df["course_completion"])
            ct_age.plot(kind="bar", stacked=True, figsize=(6,5), colormap="Set3")
            plt.title("Age Bucket vs Course Completion")
            plt.xlabel("Age Bucket")
            plt.ylabel("Count")
            plt.legend(title="Course Completed")
            plt.tight_layout()
            plt.show()

        # performance_level × course_completion
        if "performance_level" in self.df.columns:
            ct_perf = pd.crosstab(self.df["performance_level"], self.df["course_completion"])
            ct_perf.plot(kind="bar", stacked=True, figsize=(6,5), colormap="Paired")
            plt.title("Performance Level vs Course Completion")
            plt.xlabel("Performance Level")
            plt.ylabel("Count")
            plt.legend(title="Course Completed")
            plt.tight_layout()
            plt.show()


# ================================================================
# Main execution
# ================================================================
def main():
    BASE_DIR = Path(__file__).resolve().parent.parent
    CLEANED_CSV = BASE_DIR / "data" / "students_cleaned.csv"

    visualizer = DataVisualizer(csv_path=CLEANED_CSV)

    # Mandatory visualisations
    visualizer.scatter_study_vs_performance()
    visualizer.histogram_quiz_participation()
    visualizer.bar_engagement_by_completion()

    # Extended visualisations
    visualizer.boxplots_numeric()
    visualizer.histograms_distribution_stats()
    visualizer.barplots_contingency_tables()


if __name__ == "__main__":
    main()
