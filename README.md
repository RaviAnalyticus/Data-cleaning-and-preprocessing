# Task 1: Data Cleaning and Preprocessing

**Internship:** Data Analyst Internship (Elevate Labs)  
**Tool:** Python (Pandas)  
**Dataset:** Customer Personality Analysis (`marketing_campaign`)

## Objective

Clean and preprocess the marketing campaign dataset so that it is ready for further data analysis.

## Cleaning Steps

- Loaded and inspected the dataset
- Checked missing values
- Removed duplicate records
- Cleaned and standardized text values
- Renamed columns to lowercase and uniform names
- Converted `dt_customer` to datetime format
- Handled invalid `year_birth` values
- Handled extreme income outliers
- Filled missing `income` values using the median
- Fixed appropriate data types
- Performed final data quality checks

## Dataset

- **Raw rows:** 2,240
- **Raw columns:** 10
- **Cleaned rows:** 2,236
- **Cleaned columns:** 10
- **Missing values after cleaning:** 0
- **Duplicate rows after cleaning:** 0

## Files

| File | Description |
|---|---|
| `marketing_campaign-selected-columns.csv` | Raw dataset |
| `Task_cleaning.py` | Data cleaning script |
| `cleaned_marketing_campaign.csv` | Cleaned dataset |
| `README.md` | Project documentation |

## Tools Used

- Python
- Pandas
- GitHub

## How to Run

```bash
pip install pandas
python Task_cleaning.py

