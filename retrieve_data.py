import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import csv
import psycopg2
from sqlalchemy import create_engine
 
url = 'https://screener.in/company/RELIANCE/consolidated/'
webpage = requests.get(url)
soup = bs(webpage.text, 'html.parser')
 
data = soup.find('section', id="profit-loss")
tdata = data.find("table")
 
table_data = []
for row in tdata.find_all('tr'):
    row_data = []
    for cell in row.find_all(['th', 'td']):
        row_data.append(cell.text.strip())
    table_data.append(row_data)
 
with open("table_data.csv", 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(table_data)
 
df_table = pd.DataFrame(table_data)
df_table.iloc[0, 0] = 'Section'
df_table.columns = df_table.iloc[0]
df_table = df_table[1:]
 
# Ensure only valid numeric data is processed with eval
def safe_eval(val):
    try:
        return eval(val)
    except:
        return val
 
for i in df_table.iloc[:, 1:].columns:
    df_table[i] = df_table[i].str.replace(',', '').str.replace('%', '/100').apply(safe_eval)
 
db_host = "192.168.3.54"
db_name = "concourse"
db_user = "concourse_user"
db_password = "concourse_pass"
db_port = "5432"
 
engine = create_engine(f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
 
# Load the DataFrame into the PostgreSQL database
df_table.to_sql('profit_loss_data', engine, if_exists='replace', index=False)
 
print("Data loaded successfully into PostgreSQL database!")
