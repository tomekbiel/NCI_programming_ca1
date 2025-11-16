# Student Data Generator

## Project Overview
Simple Python script to generate synthetic student data for educational purposes. Part of the Programming for AI module at the National College of Ireland.

## Features
- Generate synthetic student records
- Export data to CSV format
- Simple and maintainable code structure

## Project Structure
```
NCI_programming_ca1/
├── data/               # Generated data files
│   └── students.csv    # Student records in CSV format
└── src/               
    └── data_generator.py  # Main data generation script
```

## Data Fields
- `student_id`: Unique identifier (S001, S002, etc.)
- `first_name`: Student's first name
- `last_name`: Student's last name
- `gender`: Student's gender
- Additional fields will be added as needed

## Setup Instructions

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git (for version control)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/tomekbiel/NCI_programming_ca1.git
   cd NCI_programming_ca1
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # On Windows
   # or
   # source venv/bin/activate  # On Linux/Mac
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Generate synthetic student data:
   ```bash
   python generate_data.py
   ```
   The generated data will be saved to `data/raw/students_raw.csv`

2. For interactive analysis, you can use Jupyter Notebook:
   ```bash
   pip install jupyter
   jupyter notebook
   ```

## Project Structure
```
NCI_programming_ca1/
├── data/               # Data files
│   ├── raw/           # Original, immutable data
│   ├── processed/     # Cleaned data ready for analysis
│   └── external/      # External data sources
├── src/               # Source code
│   ├── data/         # Data generation and processing
│   ├── features/     # Feature engineering
│   ├── models/       # ML models
│   └── visualization/# Visualization utilities
└── tests/            # Unit tests
```

## Project Phases
1. **Data Generation**: Create synthetic 500 student records with realistic attributes
2. **Data Cleaning**: Handle missing values, outliers, and inconsistencies
3. **Exploratory Analysis**: Understand data distributions and relationships
4. **Visualization**: Create meaningful visualizations
5. **Documentation**: Document the process and findings

## Development
To contribute to this project:
1. Create a new branch for your feature
2. Make your changes
3. Run tests (when available)
4. Submit a pull request

## Academic Integrity
This project is for educational purposes as part of the Postgraduate Diploma in Science in Artificial Intelligence at the National College of Ireland. All code and documentation should be original work, with proper attribution for any third-party resources used.

## License
This project is for academic use only.
