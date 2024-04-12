# visualization.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go


def visualize_data(df):
    # Sidebar navigation
    st.sidebar.title("Menu")
    analysis_option = st.sidebar.radio("Select Analysis", ("Introduction", "Top Companies", "Filtered Data",
                                                           "Revenue Analysis", "Employee Analysis",
                                                            "Growth Analysis"))
    
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
        # Line chart for Revenue Trends of Top Companies
        fig_line_chart = px.line(top_companies, x='Rank', y='Revenue (USD millions)', title='Revenue Trends of Top Companies')
        st.plotly_chart(fig_line_chart)
        
        st.write(top_companies)

        # 3D Scatter plot for Top Companies
        fig_3d = go.Figure(data=[go.Scatter3d(
            x=top_companies['Revenue (USD millions)'],
            y=top_companies['Employees'],
            z=top_companies['Rank'],
            text=top_companies['Name'],
            mode='markers',
            marker=dict(
                size=12,
                color=top_companies['Revenue (USD millions)'], 
                colorscale='Viridis',  
                opacity=0.8
            )
        )])

        fig_3d.update_layout(
            scene=dict(
                xaxis=dict(title='Revenue (USD millions)'),
                yaxis=dict(title='Employees'),
                zaxis=dict(title='Rank'),
            ),
            title='Exploration of Top Companies: Revenue, Employees, and Rank'
        )

        st.plotly_chart(fig_3d)
        
        st.subheader("Industry Distribution:")
        industry_distribution = df['Industry'].value_counts()
        # st.write(industry_distribution)
         # Bar chart for Industry Distribution
        fig_industry_distribution = px.bar(x=industry_distribution.index, y=industry_distribution.values, labels={'x': 'Industry', 'y': 'Count'}, title='Industry Distribution')
        st.plotly_chart(fig_industry_distribution)
    
    elif analysis_option == "Filtered Data":
        filtered_df = filter_data(df)
        if not filtered_df.empty:
            st.subheader("Filtered Data Analysis:")
            st.markdown("In this section, we analyze the data based on the selected industries.")

            revenue_analysis_placeholder = st.empty()
            employee_analysis_placeholder = st.empty()
            industry_comparison_placeholder = st.empty()
            growth_analysis_placeholder = st.empty()

            with revenue_analysis_placeholder:
                st.subheader("Revenue Analysis")
                fig_revenue_trends = px.bar(filtered_df, x='Industry', y='Revenue (USD millions)', title='Revenue Trends Across Industries')
                st.plotly_chart(fig_revenue_trends)

                top_companies_revenue = filtered_df.sort_values(by='Revenue (USD millions)', ascending=False).head(3)
                st.markdown("### Top Three Companies by Revenue:")
                st.table(top_companies_revenue[['Rank', 'Name', 'Revenue (USD millions)']])

            with employee_analysis_placeholder:
                st.subheader("Employee Analysis")
                fig_employee_distribution = px.bar(filtered_df, x='Industry', y='Employees', title='Employee Distribution Across Industries')
                st.plotly_chart(fig_employee_distribution)

                top_companies_employees = filtered_df.sort_values(by='Employees', ascending=False).head(3)
                st.markdown("### Top Three Companies by Employee Count:")
                st.table(top_companies_employees[['Rank', 'Name', 'Employees']])

            with industry_comparison_placeholder:
                st.subheader("Industry Comparison")
                fig_industry_comparison = px.scatter(filtered_df, x='Revenue (USD millions)', y='Employees', color='Industry', title='Industry Comparison: Revenue vs Employees')
                st.plotly_chart(fig_industry_comparison)

            with growth_analysis_placeholder:
                st.subheader("Growth Analysis")
                fig_growth_analysis_line = px.line(filtered_df, x='Rank', y='Revenue growth', color='Industry', title='Growth Analysis: Revenue Growth by Rank')
                st.plotly_chart(fig_growth_analysis_line)

                fig_growth_analysis_bar = px.bar(filtered_df, x='Industry', y='Revenue growth', title='Growth Analysis: Revenue Growth by Industry')
                st.plotly_chart(fig_growth_analysis_bar)

        else:
            st.write("No data available for selected filters.")


    
    elif analysis_option == "Revenue Analysis":
        filtered_df = filter_data(df)
        if not filtered_df.empty:
            # Bar chart for revenue trends across industries
            fig_revenue_trends = px.bar(filtered_df, x='Industry', y='Revenue (USD millions)', title='Revenue Trends Across Industries')
            st.plotly_chart(fig_revenue_trends)

            # Display top three companies and least two companies with their revenues
            top_companies = filtered_df.sort_values(by='Revenue (USD millions)', ascending=False).head(3)
            least_companies = filtered_df.sort_values(by='Revenue (USD millions)').head(2)

            # Donut chart for top three companies by revenue
            fig_donut = px.pie(top_companies, values='Revenue (USD millions)', names='Name', hole=0.4, title='Top Three Companies by Revenue')
            st.plotly_chart(fig_donut)

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

            # Donut chart for top three companies by employee count
            fig_donut_employee = px.pie(top_companies, values='Employees', names='Name', hole=0.4, title='Top Three Companies by Employee Count')
            st.plotly_chart(fig_donut_employee)


            st.markdown("### Least Two Companies by Employee Count:")
            st.table(least_companies[['Rank', 'Name', 'Employees']])
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
            fig_growth_analysis_line = px.line(filtered_df, x='Rank', y='Revenue growth', color='Industry', title='Growth Analysis: Revenue Growth by Rank')
            st.plotly_chart(fig_growth_analysis_line)

            # Clustered Column Chart
            fig_growth_analysis_bar = px.bar(df, x='Industry', y='Revenue growth', title='Growth Analysis: Revenue Growth by Industry')
            st.plotly_chart(fig_growth_analysis_bar)
            # 3D Scatter plot for Growth Analysis
            fig_growth_3d = px.scatter_3d(filtered_df, x='Revenue (USD millions)', y='Employees', z='Revenue growth',
                                        color='Industry', size_max=40, opacity=0.7,
                                        title='Growth Analysis: Revenue, Employees, and Growth by Industry')    
            fig_growth_3d.update_layout(scene=dict(
                xaxis_title='Revenue (USD millions)',
                yaxis_title='Employees',
                zaxis_title='Revenue Growth'
            ))
            fig_growth_3d.update_layout(width=800, height=600)
            st.plotly_chart(fig_growth_3d)
            
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