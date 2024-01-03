from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

url = 'https://en.wikipedia.org/wiki/List_of_most-streamed_artists_on_Spotify'

page = requests.get(url)

soup = BeautifulSoup(page.text,'html.parser')

table = soup.find_all('table')[3]

monthly_titles = table.find_all('th')

monthly_titles = monthly_titles[0:3]

monthly_table_titles = [title.text.strip() for title in monthly_titles]

df = pd.DataFrame(columns = monthly_table_titles)

top_50_df = df.drop(columns = 'Rank')

column_data = table.find_all('tr')

for row in column_data[1:51]:
    row_data = row.find_all('td')
    individual_row_data = [stat.text.strip() for stat in row_data]
    individual_row_data = individual_row_data[0:2]
    length = len(top_50_df)
    top_50_df.loc[length] = individual_row_data

list_50 = np.array([])
for i in np.arange(1,51):
    list_50 = np.append(list_50,i)
top_50_df = top_50_df.assign(Rank = list_50)

top_50_df = top_50_df[['Rank', 'Artist','Monthly listeners(millions)']]

top_50_df['Rank'] = top_50_df['Rank'].astype(int)

date = soup.find_all('th')[76]

text_date = date.text.strip()

text_date = text_date.split(" ")[2:]

month_convert = {
    'January': '1',
    'February': '2',
    'March': '3',
    'April': '4',
    'May': '5',
    'June': '6',
    'July': '7',
    'August': '8',
    'September': '9',
    'October': '10',
    'November': '11',
    'December': '12'
}

numerical_date = str(month_convert[text_date[0]]) + '-' + text_date[1].strip(',') + '-' + text_date[2]

date_column = np.array([])
for i in np.arange(0,50):
    date_column = np.append(date_column,numerical_date)
top_50_df = top_50_df.assign(Date = date_column)

top_50_text = top_50_df.to_csv(r'C:\Users\matth\OneDrive\Desktop\WebScrape Project\t50-1-2-24.csv', index = False)

