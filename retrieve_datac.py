import hvac
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import csv
 
# URL for the data you want to scrape
url = 'https://www.screener.in/company/RELIANCE/consolidated/'
# Perform web scraping
webpage = requests.get(url)
soup = bs(webpage.text, 'html.parser')
# Extract profit and loss data
data = soup.find('section', id="profit-loss", class_="card card-large")
tdata = data.find("table")
table_data = []
for row in tdata.find_all('tr'):
   row_data = []
   for cell in row.find_all(['th', 'td']):
       row_data.append(cell.text.strip())
   table_data.append(row_data)
# Save table data to a CSV file
with open("profit_loss.csv", 'w', newline='') as file:
   writer = csv.writer(file)
   writer.writerows(table_data)
# Load table data into DataFrame
df_table = pd.DataFrame(table_data)
df_table.columns = df_table.iloc[0]
df_table = df_table[1:]
df_table = df_table.set_index('')
df_table
# Save DataFrame to a CSV file
df_table.to_csv('profit_loss.csv')