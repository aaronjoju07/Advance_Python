import streamlit as st

st.set_page_config(
    page_title="US Companies Analysis",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
    initial_sidebar_state="collapsed",
    )
st.markdown("""
    ## About This App
    
    This web application analyzes the largest companies in the United States by revenue. Users can explore various aspects of these companies, including revenue trends, employee distribution, industry comparison, geographical distribution of company headquarters, and more.
    
    ### How it Works:
    
    1. **Data Scraping**: The data is scraped from Wikipedia's page on the list of largest companies in the United States by revenue.
            
            
    ```python 
            url = 'https://en.wikipedia.org/wiki/List_of_largest_companies_in_the_United_States_by_revenue'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    table = soup.find_all('table')[1]
    column_names = [th.text.strip() for th in table.find_all('th')]
    data = []
    for row in table.find_all('tr')[1:]:
        row_data = [td.text.strip() for td in row.find_all('td')]
        data.append(row_data)
    df = pd.DataFrame(data, columns=column_names)
    ```
    
    2. **Data Cleaning**: The scraped data is cleaned and prepared for analysis. This includes converting revenue and employee columns to numeric data types and removing unnecessary characters.
    ```python
                df['Revenue (USD millions)'] = df['Revenue (USD millions)'].str.replace(',', '').astype(float)
    df['Employees'] = df['Employees'].str.replace(',', '')  # Remove commas
    df['Employees'] = df['Employees'].str.extract('(\d+)').astype(float)  # Extract numeric values
    df['Revenue growth'] = df['Revenue growth'].str.rstrip('%').astype(float)  # Remove '%' and convert to float
            
    ```
    
    3. **Geographical Distribution**: The app visualizes the geographical distribution of company headquarters using PyDeck. Users can explore the map to see where the top companies are located across the United States.
        - Merge data with Coordinates
    ```python
            def merge_data_with_coordinates(df):
    city_coordinates_df = pd.read_csv('city_coordinates.csv')
    df['State'] = df['Headquarters'].apply(lambda x: x.split(", ")[-1])  # Extract state information
    merged_df = pd.merge(df, city_coordinates_df, left_on='State', right_on='City', how='left')
    return merged_df
    ```
    ```python
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
        get_radius=20000,
        get_fill_color=[45, 50, 80],
        pickable=True
    )

    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        map_style='light'  # Set map style to light
    )

    st.pydeck_chart(deck)
            
    ```
    4. **Analysis and Visualization**: Users can select different analysis options from the sidebar to visualize and explore the data. Options include viewing top companies, filtering data by industry, analyzing revenue trends, employee distribution, geographical analysis, and more.
    
    ### Technologies Used:
    
    - Streamlit: For building the interactive web application.
    - Pandas: For data manipulation and analysis.
    - BeautifulSoup: For web scraping.
    - PyDeck: For visualizing geographical data on maps.
    - Plotly Express: For interactive data visualization.

    """)