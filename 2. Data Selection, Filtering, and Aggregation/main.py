import pandas as pd

def print_grouped_data(data_frame, msg=''):
    print(f'{msg}:')
    print(f'{data_frame}')
    print("-" * 150 + "\n") 

def main():
    df = pd.read_csv('cleaned_airbnb_data.csv')

    # take only Manhattan and Brooklyn rows
    ftd_ngh = df.loc[df['neighbourhood_group'].isin(['Manhattan', 'Brooklyn'])]

    # filtered listings with a price greater than $100 and a number_of_reviews greater than 10
    filtered = ftd_ngh[(ftd_ngh['price'] > 100) & (ftd_ngh['number_of_reviews'] > 10)]
    print_grouped_data(filtered, "Picked dataset Only Manhattan + Brooklyn with a price greater than $100 and a number_of_reviews greater than 10")
    
    # select only neccessary columns
    selected = filtered.loc[:,['neighbourhood_group', 'price', 'minimum_nights', 'number_of_reviews', 
                               'price_category', 'availability_365', 'calculated_host_listings_count']]
    print_grouped_data(selected, "Selection necessary columns")

    # group the filtered dataset by neighbourhood_group and price_category
    grouped = selected.groupby(['neighbourhood_group', 'price_category']).agg(
        avg_price=('price', 'mean'),
        avg_min_nights=('minimum_nights', 'mean'),
        avg_number_of_reviews=('number_of_reviews', 'mean'),
        avg_availability_365=('availability_365', 'mean'),
        total_number_listings=('calculated_host_listings_count', 'sum')
    ).reset_index() 
    print_grouped_data(grouped, "Set Grouped by neighbour and price_category, also aggregated by diff functions")

    # sort the data by price in descending order and by number_of_reviews in ascending
    grouped.sort_values(['avg_price', 'avg_min_nights'], ascending=[False, True], inplace=True)
    print_grouped_data(grouped, "Sort the data by price in descending order and by number_of_reviews in ascending")

    # apply rank based on avg_price and total_listings
    grouped["neighborhoods_rank"] = grouped[["avg_price","total_number_listings"]].apply(tuple,axis=1)\
             .rank(method='dense',ascending=False).astype(int)
    print_grouped_data(grouped, "applied rank based on avg_price and total_listings")
    
    # save to csv
    grouped.to_csv('aggregated_airbnb_data.csv', index=False)


if __name__ == '__main__':
    main()