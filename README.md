# Programming for AI - CA1: E-commerce Data Analysis

## Project Overview
This project is part of the Programming for AI module in the Postgraduate Diploma in Science in Artificial Intelligence at the National College of Ireland. The project focuses on generating, cleaning, analyzing, and visualizing synthetic e-commerce data to extract meaningful business insights.

## Learning Outcomes
- Generate synthetic 500 students records 
- Clean and preprocess raw data for analysis
- Perform exploratory data analysis (EDA)
- Create meaningful visualizations
- Apply data science best practices
- Document the entire process

## Project Structure
```
NCI_AI_Project/
├── data/               # Data files
│   ├── raw/           # Original, immutable data
│   ├── processed/     # Cleaned data ready for analysis
│   └── external/      # External data sources
├── docs/              # Project documentation
├── notebooks/         # Jupyter notebooks for analysis
├── reports/           # Generated analysis and visualizations
│   └── figures/      # Generated graphics
├── src/               # Source code
│   ├── data/         # Data generation and processing
│   ├── features/     # Feature engineering
│   ├── models/       # ML models
│   └── visualization/# Visualization utilities
└── tests/            # Unit tests
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Jupyter Notebook/Lab (for interactive analysis)

### Installation
1. Clone the repository (when available)
2. Create a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # On Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Generate synthetic data:
   ```bash
   python src/data/generate_data.py
   ```
2. Run the analysis notebook:
   ```bash
   jupyter notebook notebooks/analysis.ipynb
   ```

## Project Phases
1. **Data Generation**: Create synthetic 500 students records
2. **Data Cleaning**: Handle missing values, outliers, and inconsistencies
3. **Exploratory Analysis**: Understand data distributions and relationships
4. **Visualization**: Create meaningful visualizations
5. **Documentation**: Document the process and findings

## Academic Integrity
This project is for educational purposes as part of the Postgraduate Diploma in Science in Artificial Intelligence at the National College of Ireland. All code and documentation should be original work, with proper attribution for any third-party resources used.

## License
This project is for academic use only.
