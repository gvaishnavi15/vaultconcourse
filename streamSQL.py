from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time
import os
import pandas as pd
import psycopg2  # or use sqlalchemy

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")

# Set download preferences
current_dir = os.getcwd()
prefs = {
    "download.default_directory": current_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}
chrome_options.add_experimental_option("prefs", prefs)

# Set up Chrome driver
service = Service('/usr/local/bin/chromedriver')
driver = webdriver.Chrome(service=service, options=chrome_options)

def login(username, password):
    driver.get("https://www.screener.in/company/RELIANCE/consolidated/")
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "account", " " ))]'))
    )
    login_button.click()

    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[(@id = "id_username")]'))
    )
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[(@id = "id_password")]'))
    )

    email_input.send_keys(username)
    password_input.send_keys(password)

    second_login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "icon-user", " " ))]'))
    )
    second_login_button.click()

    export = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "icon-download", " " ))]'))
    )
    export.click()

login("vaishnavigdtc@gmail.com", "GodigitalV@2000")

# Wait for the file to download
time.sleep(10)

# Find the latest downloaded Excel file
download_dir = current_dir
files = os.listdir(download_dir)
excel_files = [file for file in files if file.endswith('.xlsx')]
latest_file = max(excel_files, key=os.path.getctime)

print("Files in download directory:", files)
print("Latest Excel file downloaded:", latest_file)

# Load the Excel file into a pandas DataFrame
df = pd.read_excel(latest_file)

# Connect to PostgreSQL and insert data
conn = psycopg2.connect(
    dbname="reliance_sel",
    user="vaishnavi",
    password="vaishnavi",
    host="localhost",  # or your host
    port="5432"        # or your port
)
cur = conn.cursor()

# Assuming your table structure matches the Excel columns, insert data
# Prepare and execute the SQL insert statement for each row
insert_query = """
    INSERT INTO your_table_name (narration, date_2015, date_2016, date_2017, date_2018, date_2019, date_2020, date_2021, date_2022, date_2023, date_2024, trailing, best_case, worst_case)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

for _, row in df.iterrows():
    cur.execute(insert_query, tuple(row))

conn.commit()
cur.close()
conn.close()

print("Data inserted into PostgreSQL successfully.")
driver.quit()