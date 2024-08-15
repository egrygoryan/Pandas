import pandas as pd

def categorise_length_of_stay(min_nights):
    if min_nights <= 3:
        return "short-term"
    elif min_nights <= 14:
        return "middle-term"
    else:
        return "long-term"
    
def print_dataframe_info(data_frame, msg=''):
    print(f'{msg}:')
    print(f'{data_frame}')
    print("-" * 50 + "\n") 

def main():
    # load dataset
    df = pd.read_csv('AB_NYC_2019.csv')

    # inspect first 5 rows
    print_dataframe_info(df.head(), "Head - first 5 rows")

    # basic info about data frame
    print_dataframe_info(df.info(), "Basic Info")

    # identify columns with missing values and count the number of missing entries
    na_values_by_columns = df.isna().sum()
    print_dataframe_info(na_values_by_columns, "Missing values")

    # handle missing values 
    # if we insert pd.NaT it will be considered as a missing value
    values = {"name": "Unknown", "host_name": "Unknown", "last_review": "NaT" }
    df.fillna(values, inplace=True)
    print_dataframe_info(df[['name', 'host_name', 'last_review']], "Handle missing values")

    # Create a new column price_category and categorise it based on prices
    df['price_category'] = df['price'].apply(lambda x: 'Low' if x < 100 else ('Medium' if x < 300 else 'High'))
    print_dataframe_info(df, "Price category division")

    # Create a new column length_of_stay_category and categorise it based on minimum_nights
    df['length_of_stay_category'] = df['minimum_nights'].apply(categorise_length_of_stay)
    print_dataframe_info(df, "Stay category division")

    # ensure data frame doesn't have missing values
    any_missing_values = df[['name', 'host_name', 'last_review']].isna().any()
    print_dataframe_info(any_missing_values, "Ensure data frame doesn't have missing values")

    # ensure price is greater 0, if not => remove rows
    df_cleaned_prices = df[df['price'] != 0]
    prices_greater_0 = df_cleaned_prices[df_cleaned_prices['price'] == 0].count()
    print_dataframe_info(prices_greater_0, "Ensure any price is not 0")

    # save to csv
    df.to_csv('cleaned_airbnb_data.csv', index=False)
    
if __name__ == '__main__':
    main()