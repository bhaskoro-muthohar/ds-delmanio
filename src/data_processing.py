import pandas as pd
import numpy as np

# Load data
apps_df = pd.read_csv('data/googleplaystore.csv')
reviews_df = pd.read_csv('data/googleplaystore_user_reviews.csv')
unique_features = pd.read_csv('data/unique_features.csv')

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

apps_df['Installs'] = apps_df['Installs'].astype(str).str.replace(r'[+,]', '', regex=True).astype(int)

# Sort apps by install base to see the most downloaded apps
top_apps_by_install = apps_df.sort_values(by='Installs', ascending=False)

# Look at the top 1% of apps by installs to determine extremely popular apps
top_1_percent_threshold = top_apps_by_install['Installs'].quantile(0.99)
top_1_percent_apps = top_apps_by_install[top_apps_by_install['Installs'] >= top_1_percent_threshold]

apps_df = apps_df[~apps_df['App'].isin(top_1_percent_apps)]

# Convert 'Installs' to numeric after removing '+' and ','
apps_df['Installs'] = apps_df['Installs'].astype(str).str.replace(r'[+,]', '', regex=True).astype(int)

# Compute a popularity score perhaps as a combination of installs and rating
apps_df['Popularity_Score'] = apps_df['Rating'] * np.log1p(apps_df['Installs'])

# You may need to have a 'Last Updated' column in datetime format to do this
apps_df['Last_Updated'] = pd.to_datetime(apps_df['Last Updated'])
recent_apps = apps_df[apps_df['Last_Updated'] >= '2018-06-01']


# Merge datasets on the 'App' column, including the translated reviews
combined_df = pd.merge(apps_df, reviews_df, on='App', how='inner')

# Cleanup by dropping rows with missing values and duplicates
combined_df.dropna(subset=['Rating', 'Sentiment_Polarity', 'Sentiment', 'Translated_Review'], inplace=True)
combined_df.drop_duplicates(inplace=True)

# Calculating average sentiments while keeping the review text
avg_sentiments = combined_df.groupby('App').agg({
    'Rating': 'mean',  # We can also compute the average rating here if it's relevant
    'Sentiment_Polarity': 'mean',
    'Sentiment_Subjectivity': 'mean'
}).reset_index()

# Merge the average sentiments back to the apps DataFrame
apps_enriched_df = pd.merge(apps_df.drop(['Rating'], axis=1), avg_sentiments, on='App', how='left')

# sample_reviews['Translated_Review'] = sample_reviews['Translated_Review'].apply(lambda x: ' '.join(x))
# apps_enriched_df = pd.merge(apps_enriched_df, sample_reviews, on='App', how='left')
apps_enriched_df.drop_duplicates(inplace=True)

apps_enriched_w_unique_features_df = pd.merge(apps_enriched_df, unique_features, on='App', how='left')

apps_enriched_w_unique_features_df['Price'] = apps_enriched_w_unique_features_df['Price'].str.replace('$', '').astype(float)

apps_enriched_w_unique_features_df= apps_enriched_w_unique_features_df.drop('Last Updated', axis=1)

# Save the cleaned data
apps_enriched_w_unique_features_df.to_csv('data/cleaned_googleplaystore_data.csv', index=False)
