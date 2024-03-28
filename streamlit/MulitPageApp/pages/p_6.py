import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(page_title="MultiPageApp")
st.sidebar.success("Select any page from here")
# st.set_page_config(page_title="MultiPageApp")

# Set color codes
primary_color = '#FA7070'
secondary_color = '#2C7865'
tertiary_color = '#C6EBC5'
quaternary_color = '#A1C398'

st.markdown(
    f"""
    <style>
        .reportview-container .main .block-container{{
            max-width: 1000px;
            padding-top: 2rem;
            padding-right: 2rem;
            padding-left: 2rem;
            padding-bottom: 2rem;
        }}
        .reportview-container .main {{
            color: {secondary_color};
            background-color: {primary_color};
        }}
        .sidebar .sidebar-content {{
            background-color: {tertiary_color};
            color: {secondary_color};
        }}
        .widget-slider .stSlider .slider-content {{
            background: {primary_color};
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# Load sample data
@st.cache_data
def load_data():
    data = pd.read_csv('/Users/aaronjoju/Documents/Advance_Python/streamlit/shopping_trends.csv')
    return data

data = load_data()

# Sidebar
st.sidebar.title('Filters')
selected_categories = st.sidebar.multiselect('Select categories:', data['Category'].unique())
selected_gender = st.sidebar.selectbox('Select gender:', ['All'] + list(data['Gender'].unique()))
selected_location = st.sidebar.selectbox('Select location:', ['All'] + list(data['Location'].unique()))
selected_season = st.sidebar.selectbox('Select season:', ['All'] + list(data['Season'].unique()))
selected_rating = st.sidebar.slider('Select rating:', min_value=1, max_value=5, value=(1, 5))

# Filter data
filtered_data = data.copy()
if selected_categories:
    filtered_data = filtered_data[filtered_data['Category'].isin(selected_categories)]
if selected_gender != 'All':
    filtered_data = filtered_data[filtered_data['Gender'] == selected_gender]
if selected_location != 'All':
    filtered_data = filtered_data[filtered_data['Location'] == selected_location]
if selected_season != 'All':
    filtered_data = filtered_data[filtered_data['Season'] == selected_season]
filtered_data = filtered_data[(filtered_data['Review Rating'] >= selected_rating[0]) & 
                              (filtered_data['Review Rating'] <= selected_rating[1])]

# Main page title
st.title('Retail Analytics Dashboard')

# 1. Dashboard
st.header('Shopping Behavior Dashboard')

# Metrics: Average Age, Total Customers, Average Purchase Amount
col1, col2, col3 = st.columns(3)
col1.metric("Average Age", data['Age'].mean(), "years")
col2.metric("Total Customers", data['Customer ID'].nunique(), "")
col3.metric("Average Purchase Amount", data['Purchase Amount (USD)'].mean(), "USD")

# 2. Bar Chart - Distribution of purchases by product category
st.header('Product Category Distribution')
category_counts = filtered_data['Category'].value_counts()
bar_chart_fig = px.bar(category_counts, x=category_counts.index, y=category_counts.values,
                        labels={'x': 'Category', 'y': 'Count'}, title='Product Category Distribution',
                        color_discrete_sequence=[tertiary_color])
st.plotly_chart(bar_chart_fig, use_container_width=True)

# 3. Line Chart - Trend in sales over time
st.header('Trending Dashboard')
sales_over_time = filtered_data.groupby('Season')['Purchase Amount (USD)'].sum()
line_chart_fig = px.line(sales_over_time, x=sales_over_time.index, y=sales_over_time.values,
                         labels={'x': 'Season', 'y': 'Total Sales'}, title='Trend in Sales Over Time',
                         color_discrete_sequence=[secondary_color])
st.plotly_chart(line_chart_fig, use_container_width=True)

# 4. Scatter Plot - Relationship between customer age and average purchase amount
st.header('Customer Age vs. Average Purchase Amount')
scatter_plot_fig = px.scatter(filtered_data, x='Age', y='Purchase Amount (USD)', color='Gender',
                              labels={'Age': 'Customer Age', 'Purchase Amount (USD)': 'Average Purchase Amount'},
                              title='Relationship between Customer Age and Average Purchase Amount',
                              color_discrete_sequence=[tertiary_color, secondary_color])
st.plotly_chart(scatter_plot_fig, use_container_width=True)

# 5. Bar Chart - Frequency of Purchases
st.header('Frequency of Purchases')
frequency_counts = filtered_data['Frequency of Purchases'].value_counts()
bar_chart_freq = px.bar(frequency_counts, x=frequency_counts.index, y=frequency_counts.values,
                         labels={'x': 'Frequency', 'y': 'Count'}, title='Frequency of Purchases',
                         color_discrete_sequence=[quaternary_color])
st.plotly_chart(bar_chart_freq, use_container_width=True)
