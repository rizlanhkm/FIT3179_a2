import pandas as pd

countries = [
    "Afghanistan", "Albania", "Algeria", "Angola", "Anguilla",
    "Antigua and Barbuda", "Argentina", "Armenia", "Aruba", "Australia",
    "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh",
    "Barbados", "Belarus", "Belgium", "Belize", "Benin",
    "Bermuda", "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana",
    "Brazil", "British Virgin Islands", "Brunei", "Bulgaria", "Burkina Faso",
    "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada",
    "Cayman Islands", "Central African Rep.", "Chad", "Chile", "China",
    "Colombia", "Comoros", "Congo", "Cook Islands", "Costa Rica",
    "Côte d'Ivoire", "Croatia", "Cuba", "Cyprus", "Czechia",
    "Dem. Rep. Congo", "Denmark", "Djibouti", "Dominica", "Dominican Republic",
    "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea",
    "Estonia", "Eswatini", "Ethiopia", "Falkland Islands", "Fiji",
    "Finland", "France", "French Guiana", "French Polynesia", "Gabon",
    "Georgia", "Germany", "Ghana", "Greece", "Greenland",
    "Grenada", "Guadeloupe", "Guatemala", "Guinea", "Guinea-Bissau",
    "Guyana", "Haiti", "Honduras", "Hong Kong", "Hungary",
    "Iceland", "India", "Indonesia", "Iran", "Iraq",
    "Ireland", "Italy", "Jamaica", "Japan", "Jordan",
    "Kazakhstan", "Kenya", "Kiribati", "Kuwait", "Kyrgyzstan",
    "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia",
    "Libya", "Lithuania", "Luxembourg", "Macao", "Madagascar",
    "Malawi", "Malaysia", "Maldives", "Mali", "Malta",
    "Martinique", "Mauritania", "Mauritius", "Mexico", "Moldova",
    "Mongolia", "Morocco", "Mozambique", "Myanmar", "Namibia",
    "Nepal", "Netherlands", "New Caledonia", "New Zealand", "Nicaragua",
    "Niger", "Nigeria", "North Korea", "North Macedonia", "Norway",
    "Oman", "Pakistan", "Palau", "Palestine", "Panama",
    "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland",
    "Portugal", "Puerto Rico", "Qatar", "Romania", "Russia",
    "Rwanda", "Saint Helena, Ascension and Tristan da Cunha", "Saint Lucia",
    "Saint Pierre and Miquelon", "Saint Vincent and the Grenadines", "Samoa",
    "Saudi Arabia", "Senegal", "Serbia and Montenegro", "Sierra Leone", "Singapore",
    "Slovakia", "Slovenia", "Solomon Islands", "Somalia", "South Africa",
    "South Korea", "South Sudan", "Spain", "Sri Lanka", "Sudan",
    "Suriname", "Sweden", "Switzerland", "Syria", "Taiwan",
    "Tajikistan", "Tanzania", "Thailand", "The Gambia", "Timor-Leste",
    "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey",
    "Turkmenistan", "Turks and Caicos Islands", "Uganda", "Ukraine", "United Arab Emirates",
    "United Kingdom", "United States of America", "Uruguay", "Uzbekistan", "Vanuatu",
    "Venezuela", "Vietnam", "Western Sahara", "Yemen", "Zambia", "Zimbabwe"
]

countries_to_ignore = [
    "Curaçao",
    "Gibraltar",
    "International Aviation",
    "International Shipping",
    "Réunion",
    "Saint Kitts and Nevis",
    "São Tomé and Príncipe",
    "Seychelles"
]

# remove rows with countries to ignore and split sudan and south sudan
def process_co2_data(csv_file, valid_countries):
    # Read the CSV file
    df = pd.read_csv(csv_file)

    # Remove rows where the country is in the countries_to_ignore list
    df = df[~df['Country'].isin(countries_to_ignore)]

    split_sudan_south_sudan(csv_file)

    return df

# split sudan and south sudan
def split_sudan_south_sudan(csv_file):
    # Read the CSV file
    df = pd.read_csv(csv_file)

    # Split 'Sudan and South Sudan' row into 'Sudan' and 'South Sudan'
    sudan_south_sudan_row = df[df['Country'] == 'Sudan and South Sudan']

    if not sudan_south_sudan_row.empty:
        # Remove the original 'Sudan and South Sudan' row
        df = df[df['Country'] != 'Sudan and South Sudan']

        # Copy the row for both Sudan and South Sudan
        sudan_row = sudan_south_sudan_row.copy()
        south_sudan_row = sudan_south_sudan_row.copy()

        # Rename the countries
        sudan_row['Country'] = 'Sudan'
        south_sudan_row['Country'] = 'South Sudan'

        # Split the emissions data
        for year in sudan_south_sudan_row.columns[2:]:
            sudan_row[year] = sudan_south_sudan_row[year] * 0.8763
            south_sudan_row[year] = sudan_south_sudan_row[year] * (1 - 0.8763)

        # Append the new rows to the dataframe
        df = pd.concat([df, sudan_row, south_sudan_row], ignore_index=True)

    return df

# def process_co2_data_nerf(csv_file, country_names):
#     # Read the CSV file
#     df = pd.read_csv(csv_file)
#
#     # # Remove rows where the country is not in the provided country names
#     # df = df[df['Country'].isin(country_names)]
#
#     # Create a list to hold processed rows
#     processed_rows = []
#
#     for _, row in df.iterrows():
#         country = row['Country']
#
#         if country == "Sudan and South Sudan":
#             # Split the row into two
#             sudan_row = row.copy()
#             south_sudan_row = row.copy()
#
#             # Split the CO2 emissions values
#             sudan_row['Country'] = 'Sudan'
#             south_sudan_row['Country'] = 'South Sudan'
#
#             # Calculate the split values
#             sudan_row.iloc[2:] = row.iloc[2:] * 0.8763
#             south_sudan_row.iloc[2:] = row.iloc[2:] * 0.1237
#
#             # Append to the processed rows
#             processed_rows.append(sudan_row)
#             processed_rows.append(south_sudan_row)
#         else:
#             processed_rows.append(row)
#
#     # Create a new DataFrame from processed rows
#     processed_df = pd.DataFrame(processed_rows)
#
#     return processed_df

def calculate_total_co2_by_sector(csv_file):
    # Read the CSV file into a DataFrame
    data = pd.read_csv(csv_file)

    # Group by the 'Sector' column and sum the CO2 emissions across all countries for each sector
    # Since the years are represented in columns, we sum the rows for each sector
    co2_by_sector = data.groupby('Sector').sum(numeric_only=True)

    return co2_by_sector




# Example usage: Call the function with the path to your CSV file
csv_file_path = 'fossils_co2_total_by_country.csv'
total_co2_by_country = split_sudan_south_sudan(csv_file_path)

# Display the result
print(total_co2_by_country)

# save the csv
total_co2_by_country.to_csv('processed_fossils_co2_total_by_country.csv', index=False)


#
# result_df = process_co2_data('fossils_co2_power_by_country.csv', countries)
# print(result_df)
# result_df.to_csv('processed_fossils_co2_power_by_country.csv', index=False)

# # Example usage:
# csv_file = 'fossils_co2_transport_by_country.csv'
# processed_df = process_co2_data(csv_file, countries)
#
# # Output the result to a new CSV
# processed_df.to_csv('fossils_co2_transport_by_country_processed.csv', index=False)