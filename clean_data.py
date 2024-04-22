import pandas as pd

# Read data from CSV
df = pd.read_csv('NYC_Deaths.csv')

# Remove duplicates
df = df.drop_duplicates()

# Remove rows with NA values
df = df.dropna()

# Replace 'F' and 'M' with 'Female' and 'Male' respectively
df['Sex'] = df['Sex'].map({'F': 'Female', 'M': 'Male'})

# Store cleaned data into a new CSV file
df.to_csv('INTEGRATED-DATASET.csv', index=False)
