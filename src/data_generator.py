#!/usr/bin/env python3
"""
Student Data Generator - Skeleton

Generates synthetic student records with placeholders for future fields.
"""

from pathlib import Path
import pandas as pd
import numpy as np
from faker import Faker


class StudentGenerator:
    def __init__(self, n_students=500, seed=123, locale="en_IE"):
        """Initialize the StudentGenerator.

        Args:
            n_students (int): Number of student records to generate.
            seed (int): Random seed for reproducibility.
            locale (str): Faker locale for names/addresses.
        """
        self.n_students = n_students
        self.seed = seed
        self.fake = Faker(locale)

        # Set seeds
        np.random.seed(self.seed)
        Faker.seed(self.seed)

        # Paths
        self.BASE_DIR = Path(__file__).resolve().parent.parent
        self.DATA_DIR = self.BASE_DIR / "data"
        self.DATA_DIR.mkdir(exist_ok=True)
        self.CSV_PATH = self.DATA_DIR / "raw_students.csv"

    # -----------------------------
    # Simple, independent functions
    # -----------------------------
    @staticmethod
    def generate_student_id(idx):
        """Generate student ID (S001, S002, ...)."""
        return f"S{idx:03d}"

    @staticmethod
    def generate_email(idx):
        """Generate student email based on student number."""
        return f"x{idx:03d}@student.ncirl.ie"

    @staticmethod
    def generate_gender():
        """Generate student gender (Male/Female) with 50/50 probability."""
        return np.random.choice(["Male", "Female"])

    def generate_first_name(self, gender):
        """Generate first name based on gender using Faker."""
        if gender == "Male":
            return self.fake.first_name_male()
        else:
            return self.fake.first_name_female()

    def generate_last_name(self):
        """Generate last name using Faker."""
        return self.fake.last_name()

    @staticmethod
    def generate_age():
        """
        Generate student age (continuous distribution)
        - Majority 20-24
        - Medium 25-34
        - Few 35-45
        - Rare outliers 19 (early start) and 46-50
        - Drawn from normal distribution, capped to 20-45 except for outliers
        """
        age = int(np.random.normal(loc=22, scale=3))

        # Outlier 19
        if age < 20 and np.random.rand() < 0.05:
            return 19

        # Outlier 46-50
        if age > 45 and np.random.rand() < 0.01:
            return np.random.randint(46, 51)

        # Restrained to 20-45
        return max(20, min(age, 45))

    @staticmethod
    def generate_study_hours():
        """
        Generate weekly study hours for a student.
        - Majority distributed according to Dietrich (triangular distribution)
          around 10h/week
        - Rare outliers:
            * 3% > 100 hours
            * 2% < 0 hours
        - Controlled by single random value
        """
        hours = np.random.triangular(left=0, mode=10, right=20)

        r = np.random.rand()

        if r < 0.03:  # Upper outlier
            return np.random.uniform(100, 120)
        elif r < 0.05:  # Lower outlier (0.03+0.02)
            return np.random.uniform(-5, 0)

        return round(hours, 2)

    @staticmethod
    def generate_quiz_participation():
        """
        Generate quiz participation percentage.
        - Most students between 50-100%
        - Rare anomalies: <0% or >100%
        """
        r = np.random.rand()
        if r < 0.03:  # upper outlier
            return np.random.uniform(101, 120)
        elif r < 0.05:  # lower outlier
            return np.random.uniform(-10, 0)
        return round(np.random.uniform(50, 100), 1)

    @staticmethod
    def generate_past_performance():
        """
        Generate past performance score (0-100%).
        - Normal distribution around 70%
        - Outliers possible (0-100+)
        """
        score = np.random.normal(loc=70, scale=15)
        if np.random.rand() < 0.03:  # upper outlier
            return np.random.uniform(101, 120)
        elif np.random.rand() < 0.02:  # lower outlier
            return np.random.uniform(-10, 0)
        return int(np.clip(score, 0, 100))

    @staticmethod
    def generate_course_completed():
        """
        Generate course completion status.
        - Most students complete (True)
        - Some fail or drop (False)
        """
        return np.random.choice([True, False], p=[0.7, 0.3])

    # -----------------------------
    # Aggregate student record
    # -----------------------------
    def generate_student_record(self, idx):
        """Generate a complete student record with placeholders."""
        gender = StudentGenerator.generate_gender()
        first_name = self.generate_first_name(gender)
        last_name = self.generate_last_name()

        record = {
            "student_id": StudentGenerator.generate_student_id(idx),
            "first_name": first_name,
            "last_name": last_name,
            "gender": gender,
            "email": StudentGenerator.generate_email(idx),
            "age": StudentGenerator.generate_age(),
            "study_hours": StudentGenerator.generate_study_hours(),
            "quiz_participation": StudentGenerator.generate_quiz_participation(),
            "past_performance": StudentGenerator.generate_past_performance(),
            "course_completion": StudentGenerator.generate_course_completed()
        }
        return record

    # -----------------------------
    # Generate full dataset
    # -----------------------------
    def generate_dataset(self):
        """Generate and save the full dataset of students."""
        print(f"Generating {self.n_students} student records...")
        records = [self.generate_student_record(i + 1) for i in range(self.n_students)]
        df = pd.DataFrame(records)
        df.to_csv(self.CSV_PATH, index=False)
        print(f"\nGenerated {len(df)} student records.")
        print(f"Dataset saved to: {self.CSV_PATH}\n")
        print("Sample data:")
        print(df.head())
        return df


# -----------------------------
# Main execution
# -----------------------------
def main():
    generator = StudentGenerator(n_students=500)
    generator.generate_dataset()


if __name__ == "__main__":
    main()
