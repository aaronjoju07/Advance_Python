import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_data():
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
    return df
