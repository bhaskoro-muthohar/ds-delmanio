from textblob import TextBlob
import pandas as pd

# Load the user reviews dataset
reviews_df = pd.read_csv('data/googleplaystore_user_reviews.csv')

# Drop rows where any of the required columns have NaN values
reviews_df.dropna(subset=['Translated_Review', 'Sentiment'], inplace=True)

# Function to find unique features in reviews
def extract_features(reviews):
    features = []
    for review in reviews:
        blob = TextBlob(review)
        features.extend([np for np in blob.noun_phrases if blob.sentiment.polarity > 0.1])
    return list(set(features))

# Convert 'Translated_Review' column to string type
reviews_df['Translated_Review'] = reviews_df['Translated_Review'].astype(str)

# Group reviews by app and extract features
grouped_reviews = reviews_df.groupby('App')['Translated_Review'].apply(list)
unique_features = grouped_reviews.apply(extract_features)

unique_features.to_csv('data/unique_features.csv', index=True)