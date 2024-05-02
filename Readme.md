# Android App Recommendation Analysis

This project is a comprehensive analysis aimed at identifying Android apps that provide a unique and enjoyable user experience, based on data-driven insights. We use two datasets: `googleplaystore.csv` for app details and `googleplaystore_user_reviews.csv` for user sentiment towards these apps.

## Objectives

- Popularity: Identify apps with a significant number of installs that indicate user approval.
- Usability: Focus on apps with high user ratings.
- Novelty: Highlight newer or less universally known apps.
- Unique Strengths: Extract and discuss unique app features from user reviews.

## Data Processing

The data processing is done in Python using the pandas library. The data is loaded, cleaned, and transformed in `src/data_processing.py`. The cleaned data is then saved to a CSV file.

## Sentiment Analysis

Sentiment analysis is performed on the user reviews using the TextBlob library. The sentiment analysis code can be found in `src/sentiment_analysis.py` and `src/sentiment_analysis_v2.py`.

## Database

The cleaned and processed data is then loaded into a DuckDB database for further analysis. The code for this can be found in `src/db.py`.

## Exploratory Analysis

The exploratory analysis is done in a Jupyter notebook, `notebooks/exploratory_analysis.ipynb`, where the data is loaded, explored, and visualized.

## How to Run

1. Install the dependencies: `pip install -r requirements.txt`
2. Run the data processing script: `python src/data_processing.py`
3. Load the data into the database: `python src/db.py`
4. Run the Streamlit app: `streamlit run app.py`

## Requirements

- Python 3.7+
- pandas
- numpy
- TextBlob
- DuckDB
- Jupyter
- Streamlit

## License

This project is licensed under the terms of the MIT license.