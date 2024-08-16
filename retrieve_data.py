import requests
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine

 
 
 
# URL of the webpage to scrape
url = "https://www.screener.in/company/RELIANCE/consolidated/"
 
# Send a GET request to the URL
response = requests.get(url)
 
# Check if the request was successful
if response.status_code == 200:
    print("Page retrieved successfully.")
else:
    print(f"Failed to retrieve page. Status code: {response.status_code}")
    exit()
 
# Parse the HTML content of the page
soup = BeautifulSoup(response.content, "html.parser")
 
# Scrape the "Profit & Loss" data
profit_loss_table = soup.find("section", {"id": "profit-loss"}, class_="card card-large")
 
if profit_loss_table:
    datatable = profit_loss_table.find("table")
   
    table_data = []
    for row in datatable.find_all('tr'):
        row_data = [cell.text.strip() for cell in row.find_all(['th', 'td'])]
        table_data.append(row_data)
 
    # Convert the data into a DataFrame
    df = pd.DataFrame(table_data)
 
    # Display the DataFrame
    #+print(df)
 
    # Save the DataFrame to a CSV file
    df.to_csv("profit_m.csv", index=False)
    print("Profit & Loss data saved to 'profit_m.csv'.")
else:
    print("Profit & Loss table not found on the page.")
    exit()
 
# Clean the data
df.replace(',', '', regex=True, inplace=True)
df.replace('%', '', regex=True, inplace=True)
 
# Assuming the first row is the header and the rest is data
df.columns = df.iloc[0]
df = df.drop(0).reset_index(drop=True)
 
# Convert columns to numeric, ignoring errors
df = df.apply(lambda x: pd.to_numeric(x, errors='coerce'))
 
# Fill NaN values with 0
df.fillna(0, inplace=True)
 
# Connect to PostgreSQL database
db_host = "192.168.3.54"
db_name = "concourse"
db_user = "concourse_user"
db_password = "concourse_pass"
db_port = "5432"
 
engine = create_engine(f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
 
# Load the DataFrame into the PostgreSQL database
df.to_sql('profit_loss_data', engine, if_exists='replace', index=False)
 
print("Data loaded successfully into PostgreSQL database!")
 