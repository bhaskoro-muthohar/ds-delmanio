import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import duckdb

# Function to load data
@st.cache_resource
def load_data():
    conn = duckdb.connect(database='app_reviews.duckdb', read_only=True)
    query = "SELECT * FROM app_reviews"
    df = conn.execute(query).fetchdf()
    data = df.loc[:, ~df.columns.duplicated()]
    conn.close()
    return data

def main():
    st.title('Android App Recommendation System')
    apps_data = load_data()
    apps_data['Rating'] = apps_data['Rating'].replace('', np.nan).astype(float)

    # Interactive filters in the sidebar
    st.sidebar.header('Filter Apps')
    categories = apps_data['Category'].unique().tolist()
    selected_category = st.sidebar.selectbox('Select App Category', categories)
    rating_threshold = st.sidebar.slider('Minimum Rating Threshold', 4.0, 5.0, 4.5)
    popularity_threshold = st.sidebar.slider('Minimum Popularity Score Threshold', 50, 100, 75)

    # Filtering apps based on user input
    filtered_apps = apps_data[
        (apps_data['Category'] == selected_category) &
        (apps_data['Rating'] >= rating_threshold) &
        (apps_data['Popularity_Score'] >= popularity_threshold)
    ]

    # Displaying filtered apps
    st.header('Recommended Apps')
    if not filtered_apps.empty:
        st.dataframe(filtered_apps[['App', 'Rating', 'Popularity_Score', 'Last_Updated']])
    else:
        st.write("No apps found with the selected filters.")

    # Detailed view for a selected app
    if not filtered_apps.empty:
        app_selection = st.selectbox('Select an App for More Details', filtered_apps['App'].unique())
        app_details = filtered_apps[filtered_apps['App'] == app_selection]
        st.write("### App Details")
        st.write(app_details)

    # Display a histogram of ratings within the selected category
    st.header('Rating Distribution in Selected Category')
    fig, ax = plt.subplots()
    sns.histplot(apps_data[apps_data['Category'] == selected_category]['Rating'], bins=20, kde=False)
    plt.xlabel('Rating')
    plt.ylabel('Number of Apps')
    st.pyplot(fig)

if __name__ == '__main__':
    main()
