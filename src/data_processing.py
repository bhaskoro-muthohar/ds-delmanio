import pandas as pd
import numpy as np

# Load data
apps_df = pd.read_csv('data/googleplaystore.csv')
reviews_df = pd.read_csv('data/googleplaystore_user_reviews.csv')
unique_features = pd.read_csv('data/unique_features.csv')

apps_df.dropna(subset=['Rating'], inplace=True)
reviews_df.dropna(subset=['Sentiment'], inplace=True)

apps_df['Installs'] = apps_df['Installs'].astype(str).str.replace(r'[+,]', '', regex=True).astype(int)

top_apps_by_install = apps_df.sort_values(by='Installs', ascending=False)

top_1_percent_threshold = top_apps_by_install['Installs'].quantile(0.99)
top_1_percent_apps = top_apps_by_install[top_apps_by_install['Installs'] >= top_1_percent_threshold]

apps_df = apps_df[~apps_df['App'].isin(top_1_percent_apps)]

apps_df['Installs'] = apps_df['Installs'].astype(str).str.replace(r'[+,]', '', regex=True).astype(int)

apps_df['Popularity_Score'] = apps_df['Rating'] * np.log1p(apps_df['Installs'])

apps_df['Last_Updated'] = pd.to_datetime(apps_df['Last Updated'])
recent_apps = apps_df[apps_df['Last_Updated'] >= '2018-06-01']

combined_df = pd.merge(apps_df, reviews_df, on='App', how='inner')

combined_df.dropna(subset=['Rating', 'Sentiment_Polarity', 'Sentiment', 'Translated_Review'], inplace=True)
combined_df.drop_duplicates(inplace=True)

avg_sentiments = combined_df.groupby('App').agg({
    'Rating': 'mean',
    'Sentiment_Polarity': 'mean',
    'Sentiment_Subjectivity': 'mean'
}).reset_index()

apps_enriched_df = pd.merge(apps_df.drop(['Rating'], axis=1), avg_sentiments, on='App', how='left')

apps_enriched_df.drop_duplicates(inplace=True)

apps_enriched_w_unique_features_df = pd.merge(apps_enriched_df, unique_features, on='App', how='left')

apps_enriched_w_unique_features_df['Price'] = apps_enriched_w_unique_features_df['Price'].str.replace('$', '').astype(float)

apps_enriched_w_unique_features_df = apps_enriched_w_unique_features_df.drop('Last Updated', axis=1)

apps_enriched_w_unique_features_df.to_csv('data/cleaned_googleplaystore_data.csv', index=False)
