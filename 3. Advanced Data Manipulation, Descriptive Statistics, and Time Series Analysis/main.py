import pandas as pd

def classify_availability(availability):
    if availability < 50:
        return "Rarely Available"
    elif availability <= 200:
        return "Occasionally Available"
    else:
        return "Highly Available"
    
def print_analysis_results(data_frame, msg=''):
    print(f'{msg}:')
    print(f'{data_frame}')
    print("-" * 150 + "\n") 

def main():
    df = pd.read_csv('cleaned_airbnb_data.csv')

    # pivot_table function to create a detailed summary
    pricing_trends = df.pivot_table(index='neighbourhood_group', columns='room_type', values='price', aggfunc='mean') 
    print_analysis_results(pricing_trends, "Detailed summary after pivoting")

    # transform the dataset to a long format using the melt
    melt = df.melt(
        id_vars=['neighbourhood_group'], 
        value_vars=['price', 'minimum_nights'],  
        var_name='metric',  
        value_name='value'  
    )
    print_analysis_results(melt, "Melting columns into rows")

    # create a new column availability_status
    df['availability_status'] = df['availability_365'].apply(classify_availability)

    # analyse different trends: availability status vs  price, number_of_reviews in neighbourhood_group
    av_status_price = df.pivot_table(index='neighbourhood_group', columns='availability_status', values='price', aggfunc='mean') 
    print_analysis_results(av_status_price, "availability status vs price by neighbour")
   
    av_status_number_rev = df.pivot_table(index='neighbourhood_group', columns='availability_status', values='number_of_reviews', aggfunc='mean') 
    print_analysis_results(av_status_number_rev, "availability status vs number of reviews by neighbour")

    # basic descriptive statistics
    stats = df[['price', 'minimum_nights', 'number_of_reviews']].describe()
    print_analysis_results(stats, "Descriptive statistics")

    # convert the last_review column to a datetime 
    df['last_review'] = pd.to_datetime(df['last_review'])
    print_analysis_results(df.info(), "change last_review type")

    # set it as an index
    df.set_index('last_review', inplace=True)
    print_analysis_results(df.index, "Ensure index is added")

    #resampling data to month delta and taking agg functions
    monthly_trends = df.resample('ME').agg({
        'number_of_reviews': 'count',  
        'price': 'mean'
    })
    print_analysis_results(monthly_trends, "Monthly trends")

    # group by month and calculate average price
    avg_price_pattern_by_season = df.groupby(df.index.month).agg({
        'price': 'mean'
    })
    print_analysis_results(avg_price_pattern_by_season, "Price fluctuation by month")


if __name__ == '__main__':
    main()