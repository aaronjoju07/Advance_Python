import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import pydeck as pdk

def scrape_data():
    url = 'https://en.wikipedia.org/wiki/List_of_largest_companies_in_the_United_States_by_revenue'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    table = soup.find_all('table')[1]  # Assuming the table you want is the second one on the page
    column_names = [th.text.strip() for th in table.find_all('th')]
    data = []
    for row in table.find_all('tr')[1:]:
        row_data = [td.text.strip() for td in row.find_all('td')]
        data.append(row_data)
    df = pd.DataFrame(data, columns=column_names)
    return df

def clean_data(df):
    df['Revenue (USD millions)'] = df['Revenue (USD millions)'].str.replace(',', '').astype(float)
    df['Employees'] = df['Employees'].str.replace(',', '')  # Remove commas
    df['Employees'] = df['Employees'].str.extract('(\d+)').astype(float)  # Extract numeric values
    df['Revenue growth'] = df['Revenue growth'].str.rstrip('%').astype(float)  # Remove '%' and convert to float
    return df

def merge_data_with_coordinates(df):
    city_coordinates_df = pd.read_csv('city_coordinates.csv')
    df['State'] = df['Headquarters'].apply(lambda x: x.split(", ")[-1])  # Extract state information
    merged_df = pd.merge(df, city_coordinates_df, left_on='State', right_on='City', how='left')
    return merged_df

def plot_map(df):
    st.subheader("Geographical Distribution of Company Headquarters:")
    view_state = pdk.ViewState(
        latitude=37.0902,
        longitude=-95.7129,
        zoom=3,
        pitch=0
    )

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position=['Longitude', 'Latitude'],
        get_radius=15000,
        get_fill_color=[45, 50, 80],
        pickable=True
    )

    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        map_style='light'
    )

    st.pydeck_chart(deck)


def main():
    st.set_page_config(
    page_title="US Companies Analysis",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
    initial_sidebar_state="collapsed",
    )
    st.title("Top Revenue Generating Corporations in the USA")
    df = scrape_data()
    df = clean_data(df)

    # Sidebar filter by industry
    industries = ['All'] + list(df['Industry'].unique())
    selected_industry = st.selectbox("Select Industry", industries)

    # Sidebar filter by revenue
    min_revenue = df['Revenue (USD millions)'].min()
    max_revenue = df['Revenue (USD millions)'].max()
    revenue_range = st.slider("Select Revenue Range (USD millions)", min_revenue, max_revenue, (min_revenue, max_revenue))

    filtered_df = df if selected_industry == 'All' else df[df['Industry'] == selected_industry]
    filtered_df = filtered_df[(filtered_df['Revenue (USD millions)'] >= revenue_range[0]) & (filtered_df['Revenue (USD millions)'] <= revenue_range[1])]

    df_with_coordinates = merge_data_with_coordinates(filtered_df)
    plot_map(df_with_coordinates)

if __name__ == "__main__":
    main()
