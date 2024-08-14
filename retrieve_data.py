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
profit_loss_table = soup.find("section", {"id": "profit-loss"})  # Adjust the selector as necessary
 
if profit_loss_table:
    # Extracting table rows
    rows = profit_loss_table.find_all("tr")
 
    # Extracting the header (year) and the data
    headers = [th.text.strip() for th in rows[0].find_all("th")]
    data = []
    for row in rows[1:]:
        cols = [td.text.strip() for td in row.find_all("td")]
        data.append(cols)
 
    # Convert the data into a DataFrame
    df = pd.DataFrame(data, columns=headers)
 
    # Display the DataFrame
    print(df)
 
    # Save the DataFrame to an Excel file
    df.to_csv("reliable_profit_loss.csv", index=False)
    print("Profit & Loss data saved to 'reliable_profit_loss.csv'.")
else:
    print("Profit & Loss table not found on the page.")