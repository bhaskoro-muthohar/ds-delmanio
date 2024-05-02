import pandas as pd
import duckdb

df = pd.read_csv('data/cleaned_googleplaystore_data.csv')

df['Last_Updated'] = pd.to_datetime(df['Last_Updated']).dt.strftime('%Y-%m-%d')

df['Price'] = df['Price'].astype(str).str.replace(r'[$,]', '', regex=True).astype(float)

df.replace({'nan': None, '': None}, inplace=True)

cleaned_csv_path = 'data/cleaned_googleplaystore_data_cleaned.csv'
df.to_csv(cleaned_csv_path, index=False)

conn = duckdb.connect('app_reviews.duckdb')

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

result = conn.execute("SELECT * FROM app_reviews LIMIT 10").fetchall()
for row in result:
    print(row)

conn.close()
