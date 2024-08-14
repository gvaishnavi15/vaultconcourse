import requests
from bs4 import BeautifulSoup
import pandas as pd
 
# URL of the webpage to scrape
url = "https://www.screener.in/company/RELIABLE/consolidated/"
 
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
# Finding the table that contains the "Profit & Loss" data
profit_loss_table = soup.find("section", {"id": "profit-loss"},class_="card card-large")  # Adjust the selector as necessary
datatable= profit_loss_table.find("table")
table_data=[]
 
if profit_loss_table:
    # Extracting table rows
   table_data = []
   for row in datatable.find_all('tr'):
      row_data = []
      for cell in row.find_all(['th', 'td']):
         row_data.append(cell.text.strip())
      table_data.append(row_data)
 
    # Extracting the header (year) and the data
   #  headers = [th.text.strip() for th in rows[0].find_all("th")]
   #  data = []
   #  for row in rows[1:]:
   #      cols = [td.text.strip() for td in row.find_all("td")]
   #      data.append(cols)
 
    # Convert the data into a DataFrame
   df = pd.DataFrame(table_data)
 
    # Display the DataFrame
   print(df)
 
    # Save the DataFrame to an Excel file
   df.to_csv("reliable_profit_loss.csv", index=False)
   print("Profit & Loss data saved to 'reliable_profit_loss.csv'.")
else:
    print("Profit & Loss table not found on the page.")