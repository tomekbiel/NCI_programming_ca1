#!/usr/bin/env python3
"""
Data Cleaning & Wrangling Module

Contains functions for cleaning and preprocessing student dataset for analysis.
Designed for postgrad AI coursework: handling missing values, anomalies,
categorical transformations, normalization, and feature derivation.
"""

import pandas as pd
import numpy as np
from pathlib import Path

# Import static method for generating emails
from data_generator import StudentGenerator  # assuming it's in the same folder


class DataCleaner:
    def __init__(self, csv_path: str):
        """
        Initialize DataCleaner with path to CSV.
        Reads CSV into a pandas DataFrame.
        """
        self.csv_path = csv_path
        self.df = pd.read_csv(csv_path)

    # -----------------------------
    # 1. Duplicate handling
    # -----------------------------
    def remove_duplicates(self):
        """
        Remove duplicate rows if any.
        By default checks full-row duplicates.

        NOTE:
        - Normally our dataset should not contain duplicates.
        - Using full-row duplicate detection is usually enough.
        - If needed, you can uncomment subset=['student_id'] to remove
          multiple entries of the same student ID only.
        """

        # --- OPTIONAL: detect duplicates only by student_id ---
        # self.df.drop_duplicates(subset=['student_id'], keep='first', inplace=True)
        # print("Duplicates removed based on student_id")  # Uncomment if needed
        # return self.df

        # --- DEFAULT: remove exact full-row duplicates ---
        self.df.drop_duplicates(inplace=True)
        # print("Full-row duplicates removed")  # Optional debug
        return self.df

    # -----------------------------
    # 2. Convert data types
    # -----------------------------
    def convert_types(self):
        """
        Convert columns to appropriate types:
        - 'course_completion' → boolean
        - 'gender' → category
        - 'age' → int, will bucket later
        - Numeric columns → float
        """
        # Convert course_completion strings to boolean
        # Treat: True values = ['1', 'Yes', 'Completed', 'TRUE']
        # False values = everything else including NaN
        true_vals = ['1', 'Yes', 'Completed', 'TRUE', True]
        self.df['course_completion'] = self.df['course_completion'].apply(
            lambda x: True if x in true_vals else False
        )

        # Convert gender to category
        self.df['gender'] = self.df['gender'].astype('category')

        # Convert numeric columns
        numeric_cols = ['study_hours', 'quiz_participation', 'past_performance', 'age']
        for col in numeric_cols:
            self.df[col] = pd.to_numeric(self.df[col], errors='coerce')  # coerce to NaN if error

        return self.df

    # -----------------------------
    # 3. Missing value handling
    # -----------------------------
    def handle_missing_values(self):
        """
        Handle NaNs using appropriate strategies.

        NUMERIC:
          - study_hours, quiz_participation, past_performance → fill with median
          - age → fill median (generator rarely produces NaN)

        BOOLEAN:
          - course_completion → already converted, redundant

        TEXT / ID:
          - If email is missing but student_id exists → reconstruct via StudentGenerator.generate_email()
          - If both email and student_id missing → drop row
          - If gender missing → infer from first_name or set 'Unknown'
        """
        # === 1. NUMERIC ===
        numeric_cols = ['study_hours', 'quiz_participation', 'past_performance', 'age']
        existing_numeric_cols = [c for c in numeric_cols if c in self.df.columns]
        # Pythonic bulk fill
        self.df[existing_numeric_cols] = self.df[existing_numeric_cols].fillna(
            self.df[existing_numeric_cols].median()
        )

        # === 2. BOOLEAN ===
        # self.df['course_completion'] = self.df['course_completion'].fillna(False)  # optional

        # === 3. EMAIL reconstruction ===
        missing_email = self.df['email'].isna()
        has_id = self.df['student_id'].notna()
        # Pythonic apply -> use StudentGenerator
        self.df.loc[missing_email & has_id, 'email'] = self.df.loc[missing_email & has_id, 'student_id'] \
            .apply(StudentGenerator.generate_email)

        # Drop rows with both email and student_id missing
        self.df = self.df[~(self.df['email'].isna() & self.df['student_id'].isna())]

        # === 4. GENDER REPAIR LOGIC ===
        # Ensure 'Unknown' exists as a category (needed for categorical columns)
        if 'Unknown' not in self.df['gender'].cat.categories:
            self.df['gender'] = self.df['gender'].cat.add_categories(['Unknown'])

        # Fill missing gender
        missing_gender = self.df['gender'].isna()
        self.df.loc[missing_gender, 'gender'] = 'Unknown'

        return self.df

    # -----------------------------
    # 4. Correct anomalies / clipping
    # -----------------------------
    def correct_anomalies(self):
        """
        Correct out-of-range values or inconsistencies:
        - study_hours → clip 0–Q3 + 2*IQR (robust to outliers)
        - quiz_participation → clip 0–100
        - past_performance → clip 0–100
        """
        # --- Study hours: robust upper limit ---
        Q1 = self.df['study_hours'].quantile(0.25)
        Q3 = self.df['study_hours'].quantile(0.75)
        IQR = Q3 - Q1
        upper_limit = Q3 + 2 * IQR
        self.df['study_hours'] = self.df['study_hours'].clip(0, upper_limit)

        # --- Percentages ---
        self.df['quiz_participation'] = self.df['quiz_participation'].clip(0, 100)
        self.df['past_performance'] = self.df['past_performance'].clip(0, 100)

        return self.df

    # -----------------------------
    # 5. Feature engineering / normalization
    # -----------------------------
    def normalize_columns(self):
        """
        Normalize numeric columns to [0,1] range if needed.

        NOTE:
        This is not Z-score normalization (standardization).
        We are using min-max scaling: values are rescaled linearly
        to fit into [0,1] based on observed min and max.
        """
        self.df['study_hours_norm'] = (self.df['study_hours'] - self.df['study_hours'].min()) / \
                                      (self.df['study_hours'].max() - self.df['study_hours'].min())
        return self.df
    # -----------------------------
    # 6. Feature engineering: engagement score
    # -----------------------------

    def create_engagement(self):
        """
        Create derived column 'engagement':
        Weighted combination of normalized study_hours and quiz participation
        """
        self.df['engagement'] = 0.6 * self.df['study_hours_norm'] + 0.4 * (self.df['quiz_participation'] / 100)
        return self.df

    # -----------------------------
    # 7. Bucketing / categorical transformations
    # -----------------------------
    def bucket_age(self):
        """
        Convert age to categorical buckets:
        - 19-24, 25-34, 35-45, 46+
        """
        bins = [0, 24, 34, 45, 100]
        labels = ['19-24', '25-34', '35-45', '46+']
        self.df['age_bucket'] = pd.cut(self.df['age'], bins=bins, labels=labels, include_lowest=True)
        return self.df

    # -----------------------------
    # 8. Save cleaned data
    # -----------------------------
    def save_cleaned_data(self, output_path: str):
        """
        Save cleaned dataset to CSV.
        """
        self.df.to_csv(output_path, index=False)
        print(f"Cleaned data saved to {output_path}")
        return self.df


# -----------------------------
# Main execution / pipeline
# -----------------------------
def main():
    BASE_DIR = Path(__file__).resolve().parent.parent
    RAW_CSV = BASE_DIR / "data" / "students_raw.csv"       # TODO: change if testing another file
    CLEAN_CSV = BASE_DIR / "data" / "students_cleaned.csv" # TODO: change output name if needed

    cleaner = DataCleaner(csv_path=RAW_CSV)
    cleaner.remove_duplicates()      # optional
    cleaner.convert_types()          # convert boolean, category, numeric
    cleaner.handle_missing_values()  # median / fill / dropna
    cleaner.correct_anomalies()      # clipping, fixing inconsistencies
    cleaner.normalize_columns()      # study_hours normalization
    cleaner.create_engagement()       # derived column
    cleaner.bucket_age()             # age buckets
    cleaner.save_cleaned_data(CLEAN_CSV)

if __name__ == "__main__":
    main()
