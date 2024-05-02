import pandas as pd
import duckdb

# Load the data into a pandas DataFrame
df = pd.read_csv('data/cleaned_googleplaystore_data.csv')

# Convert the 'Last_Updated' column to datetime and reformat it
df['Last_Updated'] = pd.to_datetime(df['Last_Updated']).dt.strftime('%Y-%m-%d')

# Convert 'Price' by removing any dollar signs and converting to float
df['Price'] = df['Price'].astype(str).str.replace(r'[$,]', '', regex=True).astype(float)

# Replace any remaining 'nan' strings or empty strings with actual NaN values
df.replace({'nan': None, '': None}, inplace=True)

# Save the cleaned DataFrame back to a new CSV file
cleaned_csv_path = 'data/cleaned_googleplaystore_data_cleaned.csv'
df.to_csv(cleaned_csv_path, index=False)

# Connect to DuckDB
conn = duckdb.connect('app_reviews.duckdb')

# Create a table in DuckDB corresponding to the DataFrame structure
conn.execute("""
CREATE TABLE if not exists app_reviews (
    App VARCHAR,
    Category VARCHAR,
    Reviews INTEGER,
    Size VARCHAR,
    Installs INTEGER,
    Type VARCHAR,
    Price FLOAT,
    Content_Rating VARCHAR,
    Genres VARCHAR,
    Current_Ver VARCHAR,
    Android_Ver VARCHAR,
    Popularity_Score FLOAT,
    Last_Updated DATE,
    Rating FLOAT,
    Sentiment_Polarity FLOAT,
    Sentiment_Subjectivity FLOAT,
    Translated_Review VARCHAR
)
""")

# Import the cleaned CSV data into the table
conn.execute(f"""
COPY app_reviews FROM '{cleaned_csv_path}' 
WITH (
    HEADER,
    DELIMITER ',',
    NULL 'None',
    QUOTE '"',
    ESCAPE '"'
)
""")

# Verify the import
result = conn.execute("SELECT * FROM app_reviews LIMIT 10").fetchall()
for row in result:
    print(row)

# Close the connection when done
conn.close()
