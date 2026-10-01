

import pandas as pd

RAW_PATH = "marketing_campaign-selected-columns.csv"
CLEAN_PATH = "cleaned_marketing_campaign.csv"


# 1. LOAD + INITIAL INSPECTION

df = pd.read_csv(RAW_PATH)
raw_shape = df.shape

print("=" * 60)
print("RAW DATA")
print("=" * 60)
print("Shape          :", df.shape)
print("\nMissing values :\n", df.isnull().sum()[df.isnull().sum() > 0])
print("\nDuplicate rows :", df.duplicated().sum())
print("Duplicate IDs  :", df["ID"].duplicated().sum())
print("\nData types:\n", df.dtypes)


# 2. RENAME COLUMNS  (lowercase, no spaces)

df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")


# 3. REMOVE DUPLICATES

n_before = len(df)
df = df.drop_duplicates()                 # fully identical rows
df = df.drop_duplicates(subset="id")      # same customer ID repeated
dups_removed = n_before - len(df)


# 4. STANDARDIZE TEXT VALUES

# strip stray spaces first
for col in ["education", "marital_status"]:
    df[col] = df[col].str.strip()

# education: "2n Cycle" is the 2nd-cycle (Master's) degree -> merge with Master
df["education"] = df["education"].replace({"2n Cycle": "Master"})

# marital_status: consistent casing + fix junk / duplicate categories
df["marital_status"] = df["marital_status"].str.title()
df["marital_status"] = df["marital_status"].replace(
    {
        "Alone": "Single",   # same meaning as Single
        "Absurd": "Other",   # invalid entries
        "Yolo": "Other",     # invalid entries
    }
)


# 5. CONVERT DATE FORMAT  (string -> datetime, saved as dd-mm-yyyy)

df["dt_customer"] = pd.to_datetime(df["dt_customer"], format="%d-%m-%Y", errors="coerce")
assert df["dt_customer"].isnull().sum() == 0, "Some dates could not be parsed"


# 6. OUTLIER TREATMENT

n_before = len(df)

# (a) year_birth: customers born before 1940 would be 100+ years old
#     when this data was collected (~2014) -> invalid entries
bad_birth = df["year_birth"] < 1940
print("\nInvalid year_birth rows removed:", bad_birth.sum())
df = df[~bad_birth]

# (b) income: Tukey "extreme" fence = Q3 + 3 * IQR
q1, q3 = df["income"].quantile([0.25, 0.75])
iqr = q3 - q1
extreme_upper = q3 + 3 * iqr
bad_income = df["income"] > extreme_upper
print(f"Extreme income outliers (> {extreme_upper:,.0f}) removed:", bad_income.sum())
print(df.loc[bad_income, ["id", "income"]].to_string(index=False))
df = df[~bad_income]

outliers_removed = n_before - len(df)


# 7. HANDLE MISSING VALUES

missing_income = df["income"].isnull().sum()
median_income = df["income"].median()          # median = robust to outliers
df["income"] = df["income"].fillna(median_income)
print(f"\nMissing income filled: {missing_income} (median = {median_income:,.0f})")


# 8. FIX DATA TYPES

df["income"] = df["income"].round().astype(int)
df["education"] = df["education"].astype("category")
df["marital_status"] = df["marital_status"].astype("category")

df = df.reset_index(drop=True)


# 9. FINAL DATA-QUALITY CHECK

assert df.isnull().sum().sum() == 0
assert df.duplicated().sum() == 0
assert df["id"].is_unique

print("\n" + "=" * 60)
print("CLEANED DATA")
print("=" * 60)
print("Shape          :", df.shape)
print("Missing values :", df.isnull().sum().sum())
print("Duplicate rows :", df.duplicated().sum())
print("\nData types:\n", df.dtypes)
print("\neducation:\n", df["education"].value_counts())
print("\nmarital_status:\n", df["marital_status"].value_counts())


# 10. SAVE CLEANED DATASET

df.to_csv(CLEAN_PATH, index=False, date_format="%d-%m-%Y")

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"Rows   : {raw_shape[0]} -> {df.shape[0]}")
print(f"Columns: {raw_shape[1]} -> {df.shape[1]}")
print(f"Duplicates removed       : {dups_removed}")
print(f"Outlier rows removed     : {outliers_removed}")
print(f"Missing income filled    : {missing_income}")
print(f"Saved cleaned file as    : {CLEAN_PATH}")