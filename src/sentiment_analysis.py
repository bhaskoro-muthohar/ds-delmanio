from textblob import TextBlob
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report

# Load the user reviews dataset
reviews_df = pd.read_csv('data/googleplaystore_user_reviews.csv')

# Drop rows where any of the required columns have NaN values
reviews_df.dropna(subset=['Translated_Review', 'Sentiment'], inplace=True)

# Function to clean and analyze sentiment of reviews
def analyze_sentiment(review):
    # Clean the review text data
    review = str(review).lower().strip()
    # Analyze sentiment
    blob = TextBlob(review)
    return blob.sentiment.polarity, blob.sentiment.subjectivity

# Apply the function to each review
reviews_df[['sentiment_polarity', 'sentiment_subjectivity']] = reviews_df['Translated_Review'].apply(
    lambda x: pd.Series(analyze_sentiment(x))
)

# # Save or return the dataframe with new sentiment analysis columns
# reviews_df.to_csv('data/googleplaystore_user_reviews_with_sentiment.csv', index=False)

# Function to convert TextBlob sentiment polarity to positive, neutral, or negative
def polarity_to_sentiment(polarity):
    if polarity > 0:
        return 'Positive'
    elif polarity < 0:
        return 'Negative'
    else:
        return 'Neutral'

# Apply TextBlob sentiment analysis
reviews_df['TextBlob_Polarity'] = reviews_df['Translated_Review'].apply(lambda x: TextBlob(str(x)).sentiment.polarity)
reviews_df['TextBlob_Sentiment'] = reviews_df['TextBlob_Polarity'].apply(polarity_to_sentiment)

# Calculate the accuracy of TextBlob against the existing sentiment labels
accuracy = accuracy_score(reviews_df['Sentiment'], reviews_df['TextBlob_Sentiment'])

# Output a classification report for a detailed performance analysis
report = classification_report(reviews_df['Sentiment'], reviews_df['TextBlob_Sentiment'], target_names=['Negative', 'Neutral', 'Positive'])

print(f'Accuracy of TextBlob Sentiment Analysis: {accuracy}')
print(f'Classification Report:\n{report}')