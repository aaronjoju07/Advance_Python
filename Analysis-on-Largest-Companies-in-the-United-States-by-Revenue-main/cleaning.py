import pandas as pd

def clean_data(df):
    df['Revenue (USD millions)'] = df['Revenue (USD millions)'].str.replace(',', '').astype(float)
    df['Employees'] = df['Employees'].str.replace(',', '')  # Remove commas
    df['Employees'] = df['Employees'].str.extract('(\d+)').astype(float)  # Extract numeric values
    df['Revenue growth'] = df['Revenue growth'].str.rstrip('%').astype(float)  # Remove '%' and convert to float
    return df
