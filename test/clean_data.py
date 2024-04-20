import pandas as pd

# Read data from CSV
df = pd.read_csv('graduation_outcomes.csv')

# Replace 'n/a' with NaN
df.replace(' n/a ', pd.NA, inplace=True)

# Keep only the specified columns that exist in the DataFrame
df = df[['Cohort Year', 'Demographic', 'Total Grads Num', 'Total Regents Num', 
         'Advanced Regents Num', 'Regents w/o Advanced Num', 'Local Num',
         'Still Enrolled Num', 'Dropped Out Num']]


# Drop rows containing NaN values
df.dropna(inplace=True)

# Drop duplicates if any
df = df.drop_duplicates()

# Remove commas from numeric columns and convert them to integers
numeric_columns = ['Total Grads Num', 'Total Regents Num', 'Advanced Regents Num',
                   'Regents w/o Advanced Num', 'Local Num', 'Still Enrolled Num',
                   'Dropped Out Num']
for col in numeric_columns:
    df[col] = df[col].str.replace(',', '').astype(int)

# Store cleaned data in a new CSV file
df.to_csv('cleaned_data.csv', index=False)

# Print confirmation
print("Cleaned data has been stored in 'cleaned_data.csv'")
