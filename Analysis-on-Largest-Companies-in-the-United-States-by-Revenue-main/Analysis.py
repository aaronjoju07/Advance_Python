import streamlit as st
import pandas as pd
from scraping import scrape_data
from cleaning import clean_data
from visualization import visualize_data

def main():
    st.set_page_config(
        page_title="US Companies Analysis",
        page_icon=":chart_with_upwards_trend:",
        layout="wide"
    )
    st.title("Top Revenue Generating Corporations in the USA")
    df = scrape_data()
    df = clean_data(df)
    visualize_data(df)

if __name__ == "__main__":
    main()