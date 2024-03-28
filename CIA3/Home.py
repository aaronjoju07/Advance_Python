import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
import requests
import plotly.express as px

# Function to scrape data
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

# Function to clean and prepare data
def clean_data(df):
    df['Revenue (USD millions)'] = df['Revenue (USD millions)'].str.replace(',', '').astype(float)
    df['Employees'] = df['Employees'].str.replace(',', '')  # Remove commas
    df['Employees'] = df['Employees'].str.extract('(\d+)').astype(float)  # Extract numeric values
    df['Revenue growth'] = df['Revenue growth'].str.rstrip('%').astype(float)  # Remove '%' and convert to float
    return df

# Function to perform analysis and visualization
def analyze_data(df):    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    analysis_option = st.sidebar.radio("Select Analysis", ("Introduction", "Top Companies", "Filtered Data", "Industry Distribution", 
                                                           "Revenue Analysis", "Employee Analysis", "Geographical Analysis", 
                                                           "Industry Comparison", "Growth Analysis", "Correlation Analysis"))
    
    if analysis_option == "Introduction":
        st.sidebar.success("Select an analysis option from the sidebar.")
        st.markdown("""
        ### Introduction
        This website analyzes the largest companies in the United States by revenue. You can explore various aspects of these companies, including revenue trends, employee distribution, industry comparison, and more.
        """)
        st.markdown("""
        ### Data Overview
        Here's an overview of the scraped data
        """)
        
        # Metrics for data overview
        total_companies = len(df)
        total_revenue = df['Revenue (USD millions)'].sum()
        average_growth = df['Revenue growth'].mean()
        total_employees = df['Employees'].sum()
        # Metrics: Total Companies, Total Revenue, Average Revenue Growth, Total Employees
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Companies", total_companies)
        col2.metric("Total Revenue (USD millions)", total_revenue,"USD")
        col3.metric("Average Revenue Growth (%)", average_growth)
        col4.metric("Total Employees", total_employees)
        st.markdown("""
            Now, let me summarize the key insights from this data:
            - We have a total of **{}** companies in our dataset.
            - The combined revenue of these companies amounts to **{} million USD**.
            - On average, these companies experience a **{}%** revenue growth.
            - Collectively, these companies employ a total of **{}** individuals.
            """.format(total_companies, total_revenue, average_growth, total_employees))
        
        st.markdown("""
        ### Data Scraping
        The data for this analysis is scraped from Wikipedia's page on the [list of largest companies in the United States by revenue](https://en.wikipedia.org/wiki/List_of_largest_companies_in_the_United_States_by_revenue). BeautifulSoup library is used for web scraping.
        """)
    
    elif analysis_option == "Top Companies":
        top_companies = df.sort_values(by='Revenue (USD millions)', ascending=False).head(10)
        st.subheader("Top Companies by Revenue:")
        st.write(top_companies)
        # Line chart for Revenue Trends of Top Companies
        fig_line_chart = px.line(top_companies, x='Rank', y='Revenue (USD millions)', title='Revenue Trends of Top Companies')
        st.plotly_chart(fig_line_chart)
    
    elif analysis_option == "Filtered Data":
        industries = df['Industry'].unique()
        selected_industries = st.sidebar.multiselect("Select Industries", industries)
        if selected_industries:
            filtered_df = df[df['Industry'].isin(selected_industries)]
            st.subheader("Filtered Data:")
            st.write(filtered_df)
    
    elif analysis_option == "Industry Distribution":
        st.subheader("Industry Distribution:")
        industry_distribution = df['Industry'].value_counts()
        st.write(industry_distribution)
    
    elif analysis_option == "Revenue Analysis":
        filtered_df = filter_data(df)
        if not filtered_df.empty:
            fig_revenue_trends = px.bar(filtered_df, x='Industry', y='Revenue (USD millions)', title='Revenue Trends Across Industries')
            st.plotly_chart(fig_revenue_trends)

            # Display top three companies and least two companies with their revenues
            top_companies = filtered_df.sort_values(by='Revenue (USD millions)', ascending=False).head(3)
            least_companies = filtered_df.sort_values(by='Revenue (USD millions)').head(2)

            st.markdown("### Top Three Companies by Revenue:")
            st.table(top_companies[['Rank', 'Name', 'Revenue (USD millions)']])

            st.markdown("### Least Two Companies by Revenue:")
            st.table(least_companies[['Rank', 'Name', 'Revenue (USD millions)']])
        else:
            st.write("No data available for selected filters.")
    
    elif analysis_option == "Employee Analysis":
        filtered_df = filter_data(df)
        if not filtered_df.empty:
            fig_employee_distribution = px.bar(filtered_df, x='Industry', y='Employees', title='Employee Distribution Across Industries')
            st.plotly_chart(fig_employee_distribution)

            # Display top three companies and least two companies with their employee counts
            top_companies = filtered_df.sort_values(by='Employees', ascending=False).head(3)
            least_companies = filtered_df.sort_values(by='Employees').head(2)

            st.markdown("### Top Three Companies by Employee Count:")
            st.table(top_companies[['Rank', 'Name', 'Employees']])

            st.markdown("### Least Two Companies by Employee Count:")
            st.table(least_companies[['Rank', 'Name', 'Employees']])
        else:
            st.write("No data available for selected filters.")

    
    elif analysis_option == "Geographical Analysis":
        filtered_df = filter_data(df)
        if not filtered_df.empty:
            fig_geographical_distribution = px.scatter_geo(filtered_df, locations='Headquarters', locationmode='USA-states', title='Geographical Distribution of Headquarters')
            st.plotly_chart(fig_geographical_distribution)
        else:
            st.write("No data available for selected filters.")
    
    elif analysis_option == "Industry Comparison":
        filtered_df = filter_data(df)
        if not filtered_df.empty:
            fig_industry_comparison = px.scatter(filtered_df, x='Revenue (USD millions)', y='Employees', color='Industry', title='Industry Comparison: Revenue vs Employees')
            st.plotly_chart(fig_industry_comparison)
        else:
            st.write("No data available for selected filters.")
    
    elif analysis_option == "Growth Analysis":
        filtered_df = filter_data(df)
        if not filtered_df.empty:
            # Different graph for growth analysis
            # Multi-Line Chart
            fig_growth_analysis_line = px.line(filtered_df, x='Rank', y='Revenue growth', color='Industry', title='Growth Analysis: Revenue Growth by Rank')
            st.plotly_chart(fig_growth_analysis_line)

            # Clustered Column Chart
            fig_growth_analysis_bar = px.bar(df, x='Industry', y='Revenue growth', title='Growth Analysis: Revenue Growth by Industry')
            st.plotly_chart(fig_growth_analysis_bar)


            # st.markdown("### Analysis of Growth Analysis Chart Data:")
            # st.markdown("The scatter plot above shows the relationship between revenue growth and the number of employees for different industries. From the chart, we can observe... (add your analysis here)")

        else:
            st.write("No data available for selected filters.")
    
    elif analysis_option == "Correlation Analysis":
        st.subheader("Correlation Analysis:")
        correlation_matrix = df[['Revenue (USD millions)', 'Revenue growth', 'Employees']].corr()
        fig_heatmap = px.imshow(correlation_matrix, labels=dict(color="Correlation"), title="Correlation Heatmap")
        st.plotly_chart(fig_heatmap)

def filter_data(df):
    industries = df['Industry'].unique()
    selected_industries = st.sidebar.multiselect("Select Industries", industries)
    if selected_industries:
        filtered_df = df[df['Industry'].isin(selected_industries)]
        return filtered_df
    else:
        return df

def main():
    st.set_page_config(
        page_title="US Companies Analysis",
        page_icon=":chart_with_upwards_trend:",
        layout="wide"
    )
    st.title("Largest Companies in the United States by Revenue")
    df = scrape_data()
    df = clean_data(df)
    analyze_data(df)

if __name__ == "__main__":
    main()