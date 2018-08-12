import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    cities = ['chicago','new york city','washington']
    months = ['all','january','february','march','april','may','june','july','august','september','october','november','december']
    days = ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']

    city,month,day = '', '', ''
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while city.lower() not in cities:
        city = input("Enter the name of the city to analyze :")

    # get user input for month (all, january, february, ... , june)
    while month.lower() not in months:
        month = input("Enter the month :")
    

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while day.lower() not in days:
        day = input("Enter the day :")
    

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city.lower()])
    
    raw_data_input = 'yes'
    count_row = 0
    while raw_data_input.lower() != 'no' or raw_data_input.lower() != 'n':
        raw_data_input = input("Would you like to see unfiltered raw data ? ")
        if raw_data_input.lower() == 'no' or raw_data_input.lower() == 'n':
            break
        else:
            print(df[:][count_row:count_row+5])
            count_row += 5
        

    # convert the Start Time column to the type datetime for further calculations
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # get the month from start time
    df['month'] = df['Start Time'].dt.month

    # get the day of week from start time
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter the month based on the input provided by the user
    if month.lower() != 'all':
        months = ['january','february','march','april','may','june','july','august','september','october','november','december']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    # filter the day based on the input provided by the user
    if day.lower() != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]

    # display the most common day of week
    most_common_day_of_week = df['day_of_week'].mode()[0]

    # display the most common start hour
    df['start_hour'] = df['Start Time'].dt.hour
    most_common_start_hour = df['start_hour'].mode()[0]
    
    print("most common month :".title(),most_common_month)
    print("most common day of week :".title(),most_common_day_of_week)
    print("most common start hour :".title(),most_common_start_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]

    # display most frequent combination of start station and end station trip
    most_frequest_combination = df.groupby(['Start Station','End Station'],as_index=False).count().sort_values(by='Unnamed: 0', ascending=False)

    #print(most_frequest_combination.info())
    print("most commonly used start station :".title(),most_common_start_station)
    print("most commonly used end station :".title(),most_common_end_station)
    print("most frequent combination of start station and end station trip".title(),most_frequest_combination.head(1)[['Start Station','End Station']])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()

    print("total travel time :".title(),total_travel_time)
    print("mean travel time :".title(),mean_travel_time)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("counts of user types :".title(),user_types)
    # Display counts of gender
    try:
        gender_count = df['Gender'].value_counts()
        print("counts of gender :".title(), gender_count)
    except Exception as e:
        print("Washington data doesn't have any gender details".format(e))


    # Display earliest, most recent, and most common year of birth
    try:
        earliest = df['Birth Year'].min()
        most_recent = df['Birth Year'].max()
        most_common = df['Birth Year'].mode()[0]
        print("earliest: {}, most recent: {}, and most common year of birth: {}".format(earliest,most_recent,most_common)) 
    except Exception as e:
        print("Washington data doesn't have  birth details".format(e))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
