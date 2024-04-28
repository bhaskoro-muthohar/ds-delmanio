# Import necessary libraries
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Function to load data
@st.cache_resource(experimental_allow_widgets=True)
def load_data():
    data = pd.read_csv('data/cleaned_googleplaystore_data.csv')
    data['Installs'] = data['Installs'].str.replace('[+,]', '', regex=True).astype(int)
    filtered_apps = data[(data['Rating'] > 4.0) & 
                          (data['Installs'] > 100000) & 
                          (data['Installs'] < 5000000) & 
                          (data['Sentiment'] == 'Positive')]
    return filtered_apps

# Main function where we define the app
def main():
    st.title('Android App Market Analysis')

    # Load your data
    data = load_data()

    # Sidebar - User can select the app category
    st.sidebar.header('User Input Features')
    category = st.sidebar.multiselect('Category', data['Category'].unique())

    # Sidebar - User can select the minimum rating
    min_rating = st.sidebar.slider('Minimum Rating', 0.0, 5.0, 4.0)

    # Filtering data
    filtered_data = data if not category else data[data['Category'].isin(category)]
    filtered_data = filtered_data[filtered_data['Rating'] >= min_rating]

    # Show filtered data
    st.subheader('Filtered Android Apps')
    st.write(filtered_data)

    # Visualizations
    st.subheader('Distribution of App Ratings')
    fig1, ax1 = plt.subplots()
    sns.histplot(filtered_data['Rating'], bins=20, ax=ax1)
    st.pyplot(fig1)

    # Add more visualizations and analysis as required

# Run the main function
if __name__ == '__main__':
    main()
