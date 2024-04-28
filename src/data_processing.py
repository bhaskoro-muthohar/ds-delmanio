import pandas as pd

# Load the app data
apps_df = pd.read_csv('data/googleplaystore.csv')

# Load the user reviews data
reviews_df = pd.read_csv('data/googleplaystore_user_reviews.csv')

# # Display the first few rows of the app data
# print(apps_df.head())

# # Display the first few rows of the reviews data
# print(reviews_df.head())

# # Check data types and missing values
# print(apps_df.info())
# print(reviews_df.info())

# Handling missing values
apps_df.dropna(subset=['Rating'], inplace=True)  # Assuming we drop rows where 'Rating' is missing
reviews_df.dropna(subset=['Sentiment'], inplace=True)  # Drop rows where 'Sentiment' is missing

# Correcting data types
apps_df['Rating'] = pd.to_numeric(apps_df['Rating'], errors='coerce')

# Remove duplicates
apps_df.drop_duplicates(subset=['App'], inplace=True)
reviews_df.drop_duplicates(subset=['Translated_Review', 'App'], inplace=True)

# Merging the datasets on the 'App' column
merged_df = pd.merge(apps_df, reviews_df, on='App', how='inner')

# # Check the structure of the merged dataset
# print(merged_df.head())
# print(merged_df.info())

# Save the cleaned data
merged_df.to_csv('data/cleaned_googleplaystore_data.csv', index=False)
