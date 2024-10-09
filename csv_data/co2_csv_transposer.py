import pandas as pd

# Function to load and transpose the dataset
def transpose_years(input_csv):
    # Read the CSV file
    df = pd.read_csv(input_csv)

    # Transpose the year columns into a single column using pd.melt
    df_melted = df.melt(id_vars=["Sector", "Country"],
                        var_name="Year",
                        value_name="CO2_emission")

    # Convert the 'year' column to an integer (optional if the year is represented as a string)
    df_melted['Year'] = df_melted['Year'].astype(int)

    # Sort the data by sector and year
    df_melted = df_melted.sort_values(by=["Sector", "Year"]).reset_index(drop=True)

    return df_melted

def transpose_year_columns_for_total_by_sectors(csv_file):
    # Read the CSV file into a DataFrame
    data = pd.read_csv(csv_file)

    # Use pd.melt to transpose the year columns into rows
    # 'Sector' and 'Country' are kept as identifiers, while the year columns become rows
    melted_data = pd.melt(data, id_vars=['Sector'], var_name='Year', value_name='CO2 Emissions').sort_values(by=['Sector', 'Year'])

    return melted_data


# Example usage: Call the function with the path to your CSV file
csv_file_path = 'fossils_co2_by_sector.csv'  # Replace this with the actual file path
transposed_data = transpose_years(csv_file_path)

# Display the result
print(transposed_data)

# save the csv
transposed_data.to_csv('fossils_co2_by_sector_transposed.csv', index=False)