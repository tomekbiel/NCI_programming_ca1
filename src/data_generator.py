#!/usr/bin/env python3
"""
Student Data Generator - Enhanced for Postgrad AI

Generates synthetic student records with realistic distributions,
missing values, and inconsistencies for downstream analysis.
"""

from pathlib import Path
import pandas as pd
import numpy as np
from faker import Faker
from typing import Union


class StudentGenerator:
    def __init__(self, n_students: int = 500, seed: int = 123, locale: str = "en_IE") -> None:
        """
        Initialize the StudentGenerator.

        Args:
            n_students (int): Number of student records to generate.
            seed (int): Random seed for reproducibility.
            locale (str): Faker locale for names.
        """
        self.n_students = n_students
        self.seed = seed
        self.fake = Faker(locale)

        # Set random seeds for reproducibility
        np.random.seed(self.seed)
        Faker.seed(self.seed)

        # Paths
        self.BASE_DIR = Path(__file__).resolve().parent.parent
        self.DATA_DIR = self.BASE_DIR / "data"
        self.DATA_DIR.mkdir(exist_ok=True)
        self.CSV_PATH = self.DATA_DIR / "students_raw.csv"

    # -----------------------------
    # 1. Initialization Utilities
    # -----------------------------
    @staticmethod
    def generate_student_id(idx: int) -> str:
        """Generate student ID (S001, S002, ...)."""
        return f"S{idx:03d}"

    @staticmethod
    def generate_email(idx: Union[int, str]) -> str:
        """Generate student email based on student number (handles int or string IDs)."""
        # Extract number from ID, e.g., 'S001' → 1
        try:
            num = int(''.join(filter(str.isdigit, str(idx))))
        except ValueError:
            num = 0  # fallback if no number is found
        return f"x{num:03d}@student.ncirl.ie"

    @staticmethod
    def generate_gender() -> str:
        """Generate student gender with 50/50 probability."""
        return np.random.choice(["Male", "Female"])

    def generate_first_name(self, gender: str) -> str:
        """Generate first name based on gender."""
        return self.fake.first_name_male() if gender == "Male" else self.fake.first_name_female()

    def generate_last_name(self) -> str:
        """Generate last name."""
        return self.fake.last_name()

    # -----------------------------
    # 2. Academic Data
    # -----------------------------
    @staticmethod
    def generate_age() -> int:
        """Generate student age, majority 20-24, few outliers."""
        age = int(np.random.normal(loc=22, scale=3))
        if age < 20 and np.random.rand() < 0.05:
            return 19
        if age > 45 and np.random.rand() < 0.01:
            return np.random.randint(46, 51)
        return max(20, min(age, 45))

    @staticmethod
    def generate_study_hours() -> float:
        """Generate weekly study hours, with rare outliers."""
        hours = np.random.triangular(left=0, mode=10, right=20)
        r = np.random.rand()
        if r < 0.03:
            return np.random.uniform(100, 120)
        if r < 0.05:
            return np.random.uniform(-5, 0)
        return round(hours, 2)

    @staticmethod
    def generate_quiz_participation() -> float:
        """Generate quiz participation percentage, allow rare anomalies."""
        r = np.random.rand()
        if r < 0.03:
            return np.random.uniform(101, 120)
        if r < 0.05:
            return np.random.uniform(-10, 0)
        return round(np.random.uniform(50, 100), 1)

    @staticmethod
    def generate_past_performance() -> int:
        """Generate past performance score (0-100%) with rare outliers."""
        score = np.random.normal(loc=70, scale=15)
        if np.random.rand() < 0.03:
            return int(np.random.uniform(101, 120))
        if np.random.rand() < 0.02:
            return int(np.random.uniform(-10, 0))
        return int(np.clip(score, 0, 100))

    @staticmethod
    def generate_course_completed() -> bool:
        """Generate course completion (70% True, 30% False)."""
        return np.random.choice([True, False], p=[0.7, 0.3])

    # -----------------------------
    # 3. Data Contamination
    # -----------------------------
    def introduce_nan_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Introduce missing values strategically across columns.

        Args:
            df (pd.DataFrame): Input DataFrame

        Returns:
            pd.DataFrame: DataFrame with NaN values introduced
        """
        df = df.copy()

        # Ensure appropriate nullable dtypes
        df['study_hours'] = df['study_hours'].astype('float64')
        df['quiz_participation'] = df['quiz_participation'].astype('float64')
        df['past_performance'] = df['past_performance'].astype('float64')
        df['course_completion'] = df['course_completion'].astype('boolean')

        # -----------------------------
        # Numeric columns
        # -----------------------------
        df.loc[np.random.rand(len(df)) < 0.07, 'study_hours'] = np.nan  # 7% missing
        df.loc[np.random.rand(len(df)) < 0.06, 'quiz_participation'] = np.nan
        df.loc[np.random.rand(len(df)) < 0.05, 'past_performance'] = np.nan

        # Boolean column
        df.loc[np.random.rand(len(df)) < 0.03, 'course_completion'] = pd.NA

        # -----------------------------
        # String / categorical columns
        # -----------------------------
        df.loc[np.random.rand(len(df)) < 0.01, 'first_name'] = None
        df.loc[np.random.rand(len(df)) < 0.01, 'last_name'] = None
        df.loc[np.random.rand(len(df)) < 0.005, 'gender'] = None
        df.loc[np.random.rand(len(df)) < 0.005, 'email'] = None

        return df

    def introduce_value_inconsistencies(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Introduce value inconsistencies to simulate real-world messy data.

        Args:
            df (pd.DataFrame)

        Returns:
            pd.DataFrame
        """
        df = df.copy()

        # Age inconsistencies
        df.loc[np.random.rand(len(df)) < 0.02, 'age'] = 'unknown'

        # Study hours inconsistencies
        df.loc[np.random.rand(len(df)) < 0.02, 'study_hours'] = 'various'

        # Past performance as fraction
        mask = np.random.rand(len(df)) < 0.02
        df.loc[mask, 'past_performance'] = df.loc[mask, 'past_performance'] / 100

        # Quiz participation different formats
        def alter_quiz(x):
            choice = np.random.choice(['fraction', 'percent_sign', 'decimal'])
            if choice == 'fraction':
                return f"{x}%"
            elif choice == 'percent_sign':
                return x / 100
            return round(x / 100, 2)

        mask = np.random.rand(len(df)) < 0.03
        df.loc[mask, 'quiz_participation'] = df.loc[mask, 'quiz_participation'].apply(alter_quiz)

        return df

    def introduce_boolean_inconsistencies(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Introduce boolean inconsistencies in course_completion.

        Args:
            df (pd.DataFrame)

        Returns:
            pd.DataFrame
        """
        df = df.copy()
        bool_mask = np.random.rand(len(df)) < 0.04

        for idx in df[bool_mask].index:
            if df.loc[idx, 'course_completion'] is True:
                df.loc[idx, 'course_completion'] = np.random.choice(['Yes', '1', 'Completed', 'TRUE'])
            else:
                df.loc[idx, 'course_completion'] = np.random.choice(['No', '0', 'Incomplete', 'FALSE'])

        return df



    # -----------------------------
    # 4. Generate individual student record
    # -----------------------------
    def generate_student_record(self, idx: int) -> dict:
        """
        Generate a single student record.

        Args:
            idx (int): Student index

        Returns:
            dict: Student record
        """
        gender = self.generate_gender()
        record = {
            "student_id": self.generate_student_id(idx),
            "first_name": self.generate_first_name(gender),
            "last_name": self.generate_last_name(),
            "gender": gender,
            "email": self.generate_email(idx),
            "age": self.generate_age(),
            "study_hours": self.generate_study_hours(),
            "quiz_participation": self.generate_quiz_participation(),
            "past_performance": self.generate_past_performance(),
            "course_completion": self.generate_course_completed()
        }
        return record

    # -----------------------------
    # 5. Generate full dataset
    # -----------------------------
    def generate_dataset(self, add_nan: bool = True) -> pd.DataFrame:
        """
        Generate and save the full dataset.

        Args:
            add_nan (bool): Add NaN values or not

        Returns:
            pd.DataFrame
        """
        print(f"Generating {self.n_students} student records...")
        records = [self.generate_student_record(i + 1) for i in range(self.n_students)]
        df = pd.DataFrame(records)

        if add_nan:
            print("Introducing missing values...")
            df = self.introduce_nan_values(df)

        df.to_csv(self.CSV_PATH, index=False)
        print(f"Dataset saved to: {self.CSV_PATH}")
        print(f"Sample data:\n{df.head()}")
        return df


# -----------------------------
# Main execution
# -----------------------------
def main() -> None:
    generator = StudentGenerator(n_students=500)
    generator.generate_dataset()


if __name__ == "__main__":
    main()
