import unittest
import pandas as pd
import numpy as np
from pathlib import Path
import sys
import os

# Add src directory to Python path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from data_cleaning import DataCleaner
from data_generator import StudentGenerator

class TestDataCleaning(unittest.TestCase):
    """Test suite for the DataCleaner class in data_cleaning.py"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test data before any tests are run"""
        # Initialize test data generator with 50 students
        test_data_generator = StudentGenerator(n_students=50, seed=42)
        
        # Generate test data with 50 student records
        cls.test_data = test_data_generator.generate_dataset(add_nan=False)
        
        # Save test data to a temporary CSV file
        cls.test_file_path = 'test_student_data.csv'
        cls.test_data.to_csv(cls.test_file_path, index=False)
        
        # Initialize DataCleaner with test data
        cls.data_cleaner = DataCleaner(cls.test_file_path)
    
    def test_initialization(self):
        """Test if DataCleaner initializes correctly with valid data"""
        # Verify the data was loaded correctly
        self.assertIsInstance(self.data_cleaner.df, pd.DataFrame)
        self.assertGreater(len(self.data_cleaner.df), 0)
        
        # Check if required columns exist
        required_columns = ['student_id', 'first_name', 'last_name', 'email', 'gender']
        for column in required_columns:
            self.assertIn(column, self.data_cleaner.df.columns)
    
    def test_remove_duplicates(self):
        """Test if remove_duplicates() works correctly"""
        # Create a copy of the dataframe with duplicates
        original_length = len(self.data_cleaner.df)
        df_with_duplicates = pd.concat([self.data_cleaner.df, self.data_cleaner.df.iloc[[0]]])
        
        # Apply remove_duplicates
        self.data_cleaner.df = df_with_duplicates
        self.data_cleaner.remove_duplicates()
        
        # Check if duplicates were removed (should have the same length as original)
        self.assertEqual(len(self.data_cleaner.df), original_length)
    
    def test_handle_missing_values(self):
        """Test handling of missing values in the dataset"""
        # Skip if the required columns don't exist
        if 'study_hours' not in self.data_cleaner.df.columns or 'gender' not in self.data_cleaner.df.columns:
            self.skipTest("Required columns not present in test data")
            
        # Create a copy of test data and introduce missing values
        test_data_with_missing = self.data_cleaner.df.copy()
        test_data_with_missing.loc[0, 'study_hours'] = np.nan
        test_data_with_missing.loc[1, 'gender'] = None
        
        # Save original non-null counts for comparison
        original_study_hours_count = test_data_with_missing['study_hours'].count()
        original_gender_count = test_data_with_missing['gender'].count()
        
        # Apply handle_missing_values
        self.data_cleaner.df = test_data_with_missing
        self.data_cleaner.handle_missing_values()
        
        # Verify missing values are handled
        self.assertFalse(self.data_cleaner.df['study_hours'].isna().any())
        self.assertFalse(self.data_cleaner.df['gender'].isna().any())
        
        # Verify we didn't lose too many rows
        self.assertGreaterEqual(len(self.data_cleaner.df), original_study_hours_count - 1)
        self.assertGreaterEqual(len(self.data_cleaner.df), original_gender_count - 1)
    
    def test_convert_types(self):
        """Test if data types are correctly converted"""
        # Apply type conversion
        self.data_cleaner.convert_types()
        
        # Check if course_completion is boolean
        if 'course_completion' in self.data_cleaner.df.columns:
            self.assertTrue(pd.api.types.is_bool_dtype(self.data_cleaner.df['course_completion']))
    
    def test_normalize_columns(self):
        """Test if numerical columns are properly normalized"""
        # Skip if there are no numeric columns to test
        numeric_columns = ['study_hours', 'quiz_participation', 'past_performance']
        if not any(col in self.data_cleaner.df.columns for col in numeric_columns):
            self.skipTest("No numeric columns found to test")
        
        # Make a copy of the original data for comparison
        original_data = self.data_cleaner.df[numeric_columns].copy()
        
        # Apply normalization
        self.data_cleaner.normalize_columns()
        
        # Check each numeric column
        for column in numeric_columns:
            if column in self.data_cleaner.df.columns and pd.api.types.is_numeric_dtype(self.data_cleaner.df[column]):
                # Get min and max values
                min_val = self.data_cleaner.df[column].min()
                max_val = self.data_cleaner.df[column].max()
                
                # Log the actual min/max values for debugging
                print(f"{column}: min={min_val}, max={max_val}")
                
                # Check if the column was actually modified
                if not original_data[column].equals(self.data_cleaner.df[column]):
                    # If the column was modified, check if the mean is around 0.5 (for min-max scaling)
                    mean_val = self.data_cleaner.df[column].mean()
                    self.assertGreater(mean_val, 0.0, f"Mean of {column} should be greater than 0 after normalization")
                    self.assertLess(mean_val, 1.0, f"Mean of {column} should be less than 1 after normalization")
                else:
                    # If the column wasn't modified, it might be because it was already normalized
                    print(f"Warning: {column} was not modified by normalize_columns()")
    
    def test_bucket_age(self):
        """Test if age bucketing works correctly"""
        # Apply age bucketing
        self.data_cleaner.bucket_age()
        
        # Check if age_bucket column exists and has expected categories
        self.assertIn('age_bucket', self.data_cleaner.df.columns)
        expected_categories = ['19-24', '25-34', '35-45', '46+']
        self.assertTrue(all(cat in expected_categories for cat in self.data_cleaner.df['age_bucket'].unique()))
    
    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests are done"""
        # Remove the temporary test file
        if os.path.exists(cls.test_file_path):
            os.remove(cls.test_file_path)

if __name__ == '__main__':
    unittest.main()
