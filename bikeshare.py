print('hello world!')
print('goodbye!')


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
    name = input('Before we start, could you tell me your name? A nickname is fine too!\n')
    print('\n\nHello, ' + name + '. I have data for Chicago, New York City and Washington.')
    while True:
        city = input('Which city data would you like to see?\n')
        if city.lower() in CITY_DATA:
            break
        else:
            print('Sorry, ' + name + '. I don\'t have data for ' + city + '. Please try again and ask me about one of these cities: Chicago, New York City or Washington.')

    print('\n\nGood choice. Let\'s see some data about ' + city.title() + '. If this is not the city you want to learn about, please start again.\n\n')
    months_list = ['all', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    while True:
        month = input('Which month do you want to see stats for? Please write the name of your month of choice (data available from January to June), or "all" to view the stats for all the months I have.\n')
        if month.lower() in months_list[0:7]:
            break
        elif month.lower() in months_list[7:]:
            print('I am so sorry! I only have data for the first six months of the year. Please ask me about another month.')
        else:
            print('Oh, no! I don\'t recognize what you wrote, ' + name + '. Please try again and remember to write the name of the month you want to see stats for in full.')

    days_list = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while True:
        day = input('Now, please write the day of the week you want to see stats for, or "all" for all the days of the week.\n')
        if day.lower() in days_list:
            break
        else:
            print('Uh-oh, I don\'t recognize what you wrote. Remember to write the name of the day in full!.')
    print('\n\nThank you, ' + name + '. Please bear with me while I prepare your data.\nCity of choice: ' + city.title() + '; Month: ' + month.title() + '; Day: ' + day.title())

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
    bike_df = pd.read_csv(CITY_DATA[city])
    bike_df['Start Time'] = pd.to_datetime(bike_df['Start Time'])
    bike_df['month'] = bike_df['Start Time'].dt.month
    bike_df['day_of_week'] = bike_df['Start Time'].dt.day_name()

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        bike_df = bike_df[bike_df['month'] == month]
    if day != 'all':
        bike_df = bike_df[bike_df['day_of_week'] == day.title()]

    return bike_df

def time_stats(bike_df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    bike_df['Start Time'] = pd.to_datetime(bike_df['Start Time'])

    bike_df['month'] = bike_df['Start Time'].dt.month_name()
    most_popular_month = str(bike_df['month'].mode()[0])
    print('Most Popular Month: ' + most_popular_month)

    bike_df['day_of_week'] = bike_df['Start Time'].dt.day_name()
    most_popular_day = bike_df['day_of_week'].mode()[0]
    print('Most Popular Day of the Week: ' + most_popular_day)

    bike_df['hour'] = bike_df['Start Time'].dt.strftime('%H').add(':00')
    most_popular_hour = str(bike_df['hour'].mode()[0])
    print('Most Popular Start Hour: ' + most_popular_hour)

    print('\n\nIf you chose to filter by a certain month or day, the stats for the most popular month and most popular day will return your chosen filters. Try selecting "all" if you want to learn about the most frequent month or day!')

    print("\n\nThis took %s seconds." % (time.time() - start_time))
    print('Pretty fast, isn\'t it?!')
    print('-'*40)


def station_stats(bike_df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trips...\n')
    start_time = time.time()

    most_popular_start_station = bike_df['Start Station'].mode()[0]
    print('Most common start station: ' + most_popular_start_station)

    most_popular_end_station = bike_df['End Station'].mode()[0]
    print('Most common end station: ' + most_popular_end_station)

    most_frequent_station_combination = bike_df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print('Most frequent combination of start station and end station trip:\n' + str(most_frequent_station_combination))

    print("\n\nThis took %s seconds." % (time.time() - start_time))
    print('Two more to go!')
    print('-'*40)


def trip_duration_stats(bike_df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time = bike_df['Trip Duration'].sum()
    converted_travel_time = time.strftime('%H:%M:%S', time.gmtime(total_travel_time))
    print('Total travel time: ' + converted_travel_time + ' hours')

    mean_travel_time = bike_df['Trip Duration'].mean()
    converted_mean_time = time.strftime('%H:%M:%S', time.gmtime(mean_travel_time))
    print('Mean travel time: ' + converted_mean_time + ' hours')

    print("\n\nThis took %s seconds." % (time.time() - start_time))
    print('Bear with me a little longer...')
    print('-'*40)


def user_stats(bike_df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types = bike_df['User Type'].value_counts()
    print('Our users are:\n' + str(user_types))

    if 'Gender' in bike_df.columns:
        gender_types = bike_df['Gender'].value_counts()
        print('\n\nOur users identify themselves as:\n')
        print(gender_types)

    if 'Birth Year' in bike_df.columns:
        earliest_birth = str(int(bike_df['Birth Year'].min()))
        most_recent_birth = str(int(bike_df['Birth Year'].max()))
        most_common_birth = str(int(bike_df['Birth Year'].mode()[0]))

        print('\n\nOur eldest users are from year ' + earliest_birth + '.\nOur youngest users are from year ' + most_recent_birth + '.\nThe majority of our users were born in ' + most_common_birth + '.\nIt\'s nice to see this variety. Cycling is for everyone!')

    print("\n\nThis took %s seconds." % (time.time() - start_time))
    print('Thank you so much for staying with me until the end. I hope these stats will be useful for you.')
    print('-'*40)

def raw_data(bike_df):
    """This function asks the user if they want to see 5 rows of raw data"""
    display_raw_data = input('\nWould you like to see any raw data? Please type "yes" or "no".\n').lower()
    while display_raw_data not in ('yes', 'no'):
        display_raw_data = input('Sorry, I didn\'t get that. Please type "yes" to see raw data, or "no" to skip this.\n').lower()
    if display_raw_data == 'no':
        print('Goodbye!')
        return
    else:
        for num in range(0,len(bike_df),5):
            print(bike_df.iloc[num:num+5])
            more_raw_data = input('\nDo you want to see more raw data? Please write "yes" if you do, or "no" to finish.\n').lower()
            while more_raw_data not in ('yes', 'no'):
                more_raw_data = input('Please tell me "yes" or "no"!\n').lower()
            if more_raw_data == 'no':
                print('Goodbye!')
                break

def main():
    while True:
        city, month, day = get_filters()
        bike_df = load_data(city, month, day)

        time_stats(bike_df)
        station_stats(bike_df)
        trip_duration_stats(bike_df)
        user_stats(bike_df)
        raw_data(bike_df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
