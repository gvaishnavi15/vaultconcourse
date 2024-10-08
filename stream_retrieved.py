import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
from sqlalchemy import create_engine
import os

email=os.getenv("EMAIL")
password=os.getenv("PASSWORD")
pg_user=os.getenv("PG_USER")
pg_pass=os.getenv("PG_PASS")
pg_db=os.getenv("PG_DB")

# Start a session
session = requests.Session()

# Get the login page to retrieve the CSRF token
login_url = "https://www.screener.in/login/?"
login_page = session.get(login_url)
soup = bs(login_page.content, 'html.parser')

# Find the CSRF token in the login form (usually in a hidden input field)
csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']

# Prepare the login payload
login_payload = {
    'username': email,
    'password': password,
    'csrfmiddlewaretoken': csrf_token
}

# Include the Referer header as required
headers = {
    'Referer': login_url,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
}

# Send the login request
response = session.post(login_url, data=login_payload, headers=headers)

# Check if login was successful
if response.url == "https://www.screener.in/dash/":
    print("Login successful")

    # Now navigate to the Reliance company page
    search_url = "https://www.screener.in/company/RELIANCE/consolidated/"
    search_response = session.get(search_url)
    
    if search_response.status_code == 200:
        print("Reliance data retrieved successfully")
        soup = bs(search_response.content, 'html.parser')

        # Extract the profit-loss table
        table = soup.find('section', id="profit-loss").find("table")
        
        headers = [th.text.strip() for th in table.find_all('th')]
        rows = table.find_all('tr')
        row_data = []

        for row in rows[1:]:
            cols = row.find_all('td')
            cols = [col.text.strip() for col in cols]
            row_data.append(cols)

        df = pd.DataFrame(row_data, columns=headers)
        print(df)

        # Save the DataFrame to a CSV file (optional)
        df.to_csv('profit_and_loss.csv', index=False)

        # PostgreSQL database connection details
        db_string = "postgresql+psycopg2://concourse_user:concourse_pass@localhost:5432/postgres"
        
        # Create SQLAlchemy engine
        engine = create_engine(db_string)
        
        # Load DataFrame into PostgreSQL database
        df.to_sql('profit_loss_table_data', con=engine, index=False, if_exists='replace')
        print("Data loaded successfully into PostgreSQL database!")
        
    else:
        print("Failed to retrieve Reliance data. Status Code:", search_response.status_code)

else:
    print("Login failed. Response URL:", response.url)
