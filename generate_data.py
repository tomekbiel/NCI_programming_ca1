#!/usr/bin/env python3
"""
Script to generate synthetic student data.

This script uses the StudentGenerator class to create a dataset of synthetic
student records and save it to the data/raw directory.
"""
from src.data.data_generator import StudentGenerator

def main():
    """Generate and save synthetic student data."""
    print("Starting student data generation...")
    generator = StudentGenerator(n_students=500)
    df = generator.generate_dataset()
    print("\nData generation complete!")
    print(f"Generated {len(df)} student records.")
    print("\nSample data:")
    print(df.head())

if __name__ == "__main__":
    main()
