# About This Application
    
This web application analyzes the largest companies in the United States by revenue. Users can explore various aspects of these companies, including revenue trends, employee distribution, industry comparison, geographical distribution of company headquarters, and more.
    
## How it Works:
    
1. **Data Scraping**: The data is scraped from Wikipedia's page on the list of largest companies in the United States by revenue.
    
2. **Data Cleaning**: The scraped data is cleaned and prepared for analysis. This includes converting revenue and employee columns to numeric data types and removing unnecessary characters.
    
3. **Geographical Distribution**: The app visualizes the geographical distribution of company headquarters using PyDeck. Users can explore the map to see where the top companies are located across the United States.
    
4. **Analysis and Visualization**: Users can select different analysis options from the sidebar to visualize and explore the data. Options include viewing top companies, filtering data by industry, analyzing revenue trends, employee distribution, geographical analysis, and more.
    
## Technologies Used:
    
- Streamlit: For building the interactive web application.
- Pandas: For data manipulation and analysis.
- BeautifulSoup: For web scraping.
- PyDeck: For visualizing geographical data on maps.
- Plotly Express: For interactive data visualization.


```
streamlit run Analysis.py
```
