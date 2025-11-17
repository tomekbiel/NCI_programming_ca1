#!/usr/bin/env python3
"""
Data Visualisation Module

Generates required and extended visualisations for the cleaned student dataset.

Mandatory:
1. Scatter plot: study_hours vs past_performance, colour by course_completion
2. Histogram: quiz_participation
3. Bar chart: average engagement by course_completion

Extended:
4. Boxplots with outliers for numeric columns
5. Histograms with mean, median, skewness, kurtosis
6. Barplots for contingency tables (categorical cross-analysis)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import os

class DataVisualizer:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.df = pd.read_csv(csv_path)
        # Create reports/figures directory if it doesn't exist
        self.figures_dir = Path(__file__).resolve().parent.parent / 'reports' / 'figures'
        self.figures_dir.mkdir(parents=True, exist_ok=True)
        
    def save_figure(self, fig, filename: str):
        """
        Save the given figure to the reports/figures directory.
        
        Args:
            fig: Matplotlib figure object to save
            filename: Name of the file (without extension)
            
        Returns:
            str: Full path to the saved figure
        """
        # Ensure the filename ends with .png
        if not filename.endswith('.png'):
            filename += '.png'
            
        # Create the full path
        filepath = self.figures_dir / filename
        
        # Save the figure
        fig.savefig(filepath, dpi=300, bbox_inches='tight')
        print(f"Figure saved to: {filepath}")
        return str(filepath)

    # ================================================================
    # 1. Scatter plot: study_hours vs past_performance
    # ================================================================
    def scatter_study_vs_performance(self, save_fig: bool = True, show: bool = True):
        """
        Create a scatter plot of study hours vs past performance.
        
        Args:
            save_fig: Whether to save the figure to a file
            show: Whether to display the figure
        """
        fig, ax = plt.subplots(figsize=(8,6))
        sns.scatterplot(
            data=self.df,
            x="study_hours",
            y="past_performance",
            hue="course_completion",
            style="course_completion",
            palette="Set1",
            s=60,
            ax=ax
        )
        ax.set_title("Study Hours vs Past Performance")
        ax.set_xlabel("Study Hours")
        ax.set_ylabel("Past Performance (%)")
        ax.legend(title="Course Completed")
        ax.grid(True)
        plt.tight_layout()
        
        if save_fig:
            self.save_figure(fig, "study_vs_performance.png")
        if show:
            plt.show()
        plt.close(fig)

    # ================================================================
    # 2. Histogram: quiz_participation
    # ================================================================
    def histogram_quiz_participation(self, save_fig: bool = True, show: bool = True):
        """
        Create a histogram of quiz participation.
        
        Args:
            save_fig: Whether to save the figure to a file
            show: Whether to display the figure
        """
        fig, ax = plt.subplots(figsize=(8,6))
        sns.histplot(self.df["quiz_participation"], bins=20, kde=True, color="skyblue", ax=ax)
        ax.set_title("Distribution of Quiz Participation")
        ax.set_xlabel("Quiz Participation (%)")
        ax.set_ylabel("Count")
        ax.grid(axis="y")
        plt.tight_layout()
        
        if save_fig:
            self.save_figure(fig, "quiz_participation_histogram.png")
        if show:
            plt.show()
        plt.close(fig)

    # ================================================================
    # 3. Bar chart: average engagement by course_completion
    # ================================================================
    def bar_engagement_by_completion(self, save_fig: bool = True, show: bool = True):
        """
        Create a bar plot of average engagement by course completion status.
        
        Args:
            save_fig: Whether to save the figure to a file
            show: Whether to display the figure
        """
        fig, ax = plt.subplots(figsize=(6,5))
        mean_engagement = self.df.groupby("course_completion")["engagement"].mean().reset_index()
        sns.barplot(
            data=mean_engagement,
            x="course_completion",
            y="engagement",
            palette="pastel",
            ax=ax
        )
        ax.set_title("Average Engagement by Course Completion")
        ax.set_xlabel("Course Completed")
        ax.set_ylabel("Average Engagement")
        ax.set_ylim(0,1)
        plt.tight_layout()
        
        if save_fig:
            self.save_figure(fig, "engagement_by_completion.png")
        if show:
            plt.show()
        plt.close(fig)

    # ================================================================
    # 4. Boxplots with outliers for numeric variables
    # ================================================================
    def boxplots_numeric(self, save_fig: bool = True, show: bool = True):
        """
        Create boxplots for all numeric variables.
        
        Args:
            save_fig: Whether to save the figure to a file
            show: Whether to display the figure
        """
        numeric_cols = ["study_hours", "quiz_participation", "past_performance", "engagement"]
        fig, ax = plt.subplots(figsize=(10,6))
        sns.boxplot(data=self.df[numeric_cols], palette="Set3", ax=ax)
        ax.set_title("Boxplots of Numeric Variables (outliers included)")
        ax.set_ylabel("Values")
        plt.xticks(rotation=15)
        plt.tight_layout()
        
        if save_fig:
            self.save_figure(fig, "numeric_boxplots.png")
        if show:
            plt.show()
        plt.close(fig)

    # ================================================================
    # 5. Histograms with mean, median, skewness, kurtosis
    # ================================================================
    def histograms_distribution_stats(self, save_fig: bool = True, show: bool = True):
        """
        Create histograms with distribution statistics for all numeric variables.
        
        Args:
            save_fig: Whether to save the figures to files
            show: Whether to display the figures
        """
        numeric_cols = ["study_hours", "quiz_participation", "past_performance", "engagement"]
        for col in numeric_cols:
            if col not in self.df.columns:
                print(f"Skipping {col} - column not found in data")
                continue
                
            fig, ax = plt.subplots(figsize=(8,5))
            sns.histplot(self.df[col], bins=20, kde=True, color="lightgreen", ax=ax)
            mean = self.df[col].mean()
            median = self.df[col].median()
            skew = self.df[col].skew()
            kurt = self.df[col].kurtosis()
            
            ax.axvline(mean, color='red', linestyle='--', label=f"Mean={mean:.2f}")
            ax.axvline(median, color='blue', linestyle='-', label=f"Median={median:.2f}")
            ax.set_title(f"{col} distribution (skew={skew:.2f}, kurtosis={kurt:.2f})")
            ax.set_xlabel(col)
            ax.set_ylabel("Count")
            ax.legend()
            plt.tight_layout()
            
            if save_fig:
                self.save_figure(fig, f"{col}_distribution.png")
            if show:
                plt.show()
            plt.close(fig)

    # ================================================================
    # 6. Barplots for contingency tables (categorical variables)
    # ================================================================
    def barplots_contingency_tables(self, save_fig: bool = True, show: bool = True):
        """
        Create bar plots for contingency tables of categorical variables.
        
        Args:
            save_fig: Whether to save the figures to files
            show: Whether to display the figures
        """
        # gender × course_completion
        if "gender" in self.df.columns and "course_completion" in self.df.columns:
            fig, ax = plt.subplots(figsize=(6,5))
            ct_gender = pd.crosstab(self.df["gender"], self.df["course_completion"])
            ct_gender.plot(kind="bar", stacked=True, colormap="Set2", ax=ax)
            ax.set_title("Gender vs Course Completion")
            ax.set_xlabel("Gender")
            ax.set_ylabel("Count")
            ax.legend(title="Course Completed")
            plt.tight_layout()
            
            if save_fig:
                self.save_figure(fig, "gender_vs_completion.png")
            if show:
                plt.show()
            plt.close(fig)

        # age_bucket × course_completion
        if "age_bucket" in self.df.columns and "course_completion" in self.df.columns:
            fig, ax = plt.subplots(figsize=(6,5))
            ct_age = pd.crosstab(self.df["age_bucket"], self.df["course_completion"], 
                               normalize='index' if 'normalized' in self.df.columns else 'all')
            ct_age.plot(kind="bar", stacked=True, colormap="Set3", ax=ax)
            ax.set_title("Age Bucket vs Course Completion")
            ax.set_xlabel("Age Bucket")
            ax.set_ylabel("Proportion" if 'normalized' in self.df.columns else "Count")
            ax.legend(title="Course Completed")
            plt.tight_layout()
            
            if save_fig:
                self.save_figure(fig, "age_vs_completion.png")
            if show:
                plt.show()
            plt.close(fig)

        # performance_level × course_completion
        if "performance_level" in self.df.columns and "course_completion" in self.df.columns:
            fig, ax = plt.subplots(figsize=(8,5))
            ct_perf = pd.crosstab(self.df["performance_level"], self.df["course_completion"])
            ct_perf.plot(kind="bar", stacked=True, colormap="Paired", ax=ax)
            ax.set_title("Performance Level vs Course Completion")
            ax.set_xlabel("Performance Level")
            ax.set_ylabel("Count")
            ax.legend(title="Course Completed")
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            
            if save_fig:
                self.save_figure(fig, "performance_vs_completion.png")
            if show:
                plt.show()
            plt.close(fig)


# ================================================================
# Main execution
# ================================================================
def main():
    BASE_DIR = Path(__file__).resolve().parent.parent
    CLEANED_CSV = BASE_DIR / "data" / "students_cleaned.csv"

    # Create visualizer and ensure output directory exists
    visualizer = DataVisualizer(csv_path=CLEANED_CSV)
    print(f"Saving visualizations to: {visualizer.figures_dir}")

    # Mandatory visualisations
    print("\nGenerating mandatory visualizations...")
    visualizer.scatter_study_vs_performance(save_fig=True, show=False)
    visualizer.histogram_quiz_participation(save_fig=True, show=False)
    visualizer.bar_engagement_by_completion(save_fig=True, show=False)

    # Extended visualisations
    print("\nGenerating extended visualizations...")
    visualizer.boxplots_numeric(save_fig=True, show=False)
    visualizer.histograms_distribution_stats(save_fig=True, show=False)
    visualizer.barplots_contingency_tables(save_fig=True, show=False)
    
    print("\nAll visualizations have been generated and saved.")


if __name__ == "__main__":
    main()
