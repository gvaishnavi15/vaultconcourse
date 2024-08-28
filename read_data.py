import pandas as pd
import openpyxl
import os

def read_profit_and_loss_data(file_name):
    # Check if the file exists
    if file_name and os.path.exists(file_name):
        try:
            # Load the Excel file using openpyxl
            workbook = openpyxl.load_workbook(file_name, data_only=True)

            # Select the 'datasheet' sheet
            sheet = workbook['datasheet']

            # Initialize an empty list to collect rows of the "Profit & Loss" data
            data = []
            start_collecting = False

            # Iterate through the rows in the sheet
            for row in sheet.iter_rows(values_only=True):
                # Check if this row contains the "Profit & Loss" marker
                if start_collecting:
                    if all(cell is None for cell in row):
                        break # Stop if an empty row is found after starting data collection
                    data.append(row)
                if 'Profit & Loss' in row:
                    start_collecting = True # Start collecting data from the next row

            # Convert the collected data into a DataFrame
            df_profit_loss = pd.DataFrame(data[1:], columns=data[0]) # Assumes the first row after marker is header

            # Display the first few rows
            print("Profit and Loss Data:")
            print(df_profit_loss.head())

        except Exception as e:
            print(f"Error reading Excel file or extracting Profit and Loss tab: {e}")
    else:
        print(f"File {file_name} not found or path is incorrect.")

if __name__ == '__main__':
    # Path to the downloaded Excel file
    file_name = os.path.join(os.getcwd(), "Reliance Industr.xlsx") # Adjust filename as necessary
    read_profit_and_loss_data(file_name)