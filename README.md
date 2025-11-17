# Student Data Analysis Project

## Project Overview
A comprehensive data analysis project for processing and analyzing synthetic student data. This project is part of the Programming for AI module at the National College of Ireland, demonstrating data generation, cleaning, analysis, and visualization techniques.

## Features
- **Data Generation**: Create realistic synthetic student records
- **Data Cleaning**: Handle missing values, outliers, and data inconsistencies
- **Data Analysis**: Perform statistical analysis and derive insights
- **Visualization**: Generate meaningful visualizations of student data
- **Diagnostics**: Provide data quality assessment and diagnostics

## Project Structure
```
NCI_programming_ca1/
├── data/               # Data files
│   ├── raw/           # Original, immutable data
│   ├── processed/     # Cleaned data ready for analysis
│   └── external/      # External data sources
├── docs/              # Project documentation
├── notebooks/         # Jupyter notebooks for analysis
├── reports/           # Generated analysis reports and visualizations
├── src/               # Source code
│   ├── analysis.py       # Data analysis functions
│   ├── data_cleaning.py  # Data cleaning utilities
│   ├── data_diagnosis.py # Data quality assessment
│   ├── data_generator.py # Synthetic data generation
│   └── visualization.py  # Data visualization utilities
└── tests/             # Test files
    └── test_data_cleaning.py  # Unit tests for data cleaning
```

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
   python -m venv .venv
   .\.venv\Scripts\activate  # On Windows
   # or
   # source .venv/bin/activate  # On Linux/Mac
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Data Generation
```bash
python -m src.data_generator
```
Generates synthetic student data and saves it to `data/raw/students_raw.csv`

### Data Cleaning
```bash
python -m src.data_cleaning
```
Processes raw data, handles missing values, and saves cleaned data to `data/processed/`

### Data Analysis
```bash
python -m src.analysis
```
Performs statistical analysis on the cleaned data

### Visualization
```bash
python -m src.visualization
```
Generates various visualizations and saves them to the `reports/` directory

### Data Quality Assessment
```bash
python -m src.data_diagnosis
```
Provides a comprehensive report on data quality and potential issues

### Running Tests
```bash
pytest tests/
```
Runs the test suite to ensure code quality and functionality

## Project Modules

### 1. Data Generation (`src/data_generator.py`)
- Generates synthetic student records with realistic attributes
- Includes academic performance, personal information, and course enrollment
- Outputs data in CSV format for further processing

### 2. Data Cleaning (`src/data_cleaning.py`)
- Handles missing values and outliers
- Standardizes data formats
- Validates data integrity
- Outputs cleaned datasets for analysis

### 3. Data Analysis (`src/analysis.py`)
- Performs statistical analysis
- Calculates key metrics and KPIs
- Identifies trends and patterns in student performance

### 4. Data Visualization (`src/visualization.py`)
- Creates various plots and charts
- Generates reports and dashboards
- Visualizes relationships between variables

### 5. Data Diagnosis (`src/data_diagnosis.py`)
- Assesses data quality
- Identifies potential issues and anomalies
- Provides data profiling and summary statistics

## Dependencies
- pandas >= 2.0.0
- numpy >= 1.24.0
- scipy >= 1.10.0
- Faker >= 18.0.0
- matplotlib >= 3.7.0
- seaborn >= 0.12.0
- python-dotenv >= 1.0.0

## Development

### Contributing
To contribute to this project:
1. Create a new branch for your feature
2. Make your changes
3. Run tests: `pytest tests/`
4. Ensure code style compliance: `pylint src/`
5. Submit a pull request

### Testing
Run the test suite:
```bash
pytest tests/
```

### Code Style
This project follows PEP 8 style guidelines. Please ensure your code adheres to these standards before submitting changes.

## Academic Integrity
This project is for educational purposes as part of the Postgraduate Diploma in Science in Artificial Intelligence at the National College of Ireland. All code and documentation should be original work, with proper attribution for any third-party resources used.

## License
This project is for academic use only.
