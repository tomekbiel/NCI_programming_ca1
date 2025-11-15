from pathlib import Path
import pandas as pd
import numpy as np
from faker import Faker

class StudentGenerator:
    def __init__(self, n_students=500):
        self.n_students = n_students
        self.fake = Faker()
        self.BASE_DIR = Path(__file__).resolve().parent.parent
        self.RAW_DATA_DIR = self.BASE_DIR / "data" / "raw"
        self.RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.RAW_CSV_PATH = self.RAW_DATA_DIR / "students_raw.csv"

    def generate_student_id(self, idx):
        return f"S{idx:03d}"

    def generate_gender(self):
        return np.random.choice(["Male", "Female"])

    def generate_first_name(self, gender):
        if gender == "Male":
            return self.fake.first_name_male()
        else:
            return self.fake.first_name_female()

    def generate_last_name(self):
        return self.fake.last_name()

    # Tutaj później pozostałe generate_* (age, study_hours, etc.)

    def generate_student_record(self, idx):
        gender = self.generate_gender()
        return {
            "student_id": self.generate_student_id(idx),
            "first_name": self.generate_first_name(gender),
            "last_name": self.generate_last_name(),
            "gender": gender,
            # tutaj age, study_hours...
        }

    def generate_dataset(self):
        records = [self.generate_student_record(i+1) for i in range(self.n_students)]
        df = pd.DataFrame(records)
        df.to_csv(self.RAW_CSV_PATH, index=False)
        print(f"Dataset saved to: {self.RAW_CSV_PATH}")
        return df

if __name__ == "__main__":
    generator = StudentGenerator()
    generator.generate_dataset()
