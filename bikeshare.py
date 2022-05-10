import time
import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None  # to bypass the chained assignment warning

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
weekday_dict = {'sunday':1, 'monday':2, 'tuesday':3, 'wednesday':4, 'thursday':5, 'friday':6, 'saturday':7}
months_dict = {'january':1, 'february':2, 'march':3, 'april':4, 'may':5, 'june':6}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ''
    try:
        while city not in  CITY_DATA:
            city = input('would you like to see data for Chicago, New York city or Washington? ').lower().strip()
            if city in CITY_DATA:
                break
        print('looks like you would like to see data for {}'.format(city))
    except :
        print('Invalid input ')

    # get user input for month (all, january, february, ... , june)
    month = ''
    try:
        while (month not in  months_dict) and (month != 'all'):
            month = input('which month would you like to see data for? January, February, ..., June or all? ').lower().strip()
    except :
        print('Invalid input')
    print('looks like you would like to see data for {}'.format(month))

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day=''
    while (day not in  weekday_dict) and (day != 'all'):
        try:
            day = input('which day of the week would you like to see data for? monday, tuesday, ... sunday or all? ').lower().strip()
        except :
            print('Invalid input')
    print('looks like you would like to see data for {}'.format(day))

    if day == 'all':
        day = 'all days'
    if month =='all':
        month = 'all months'
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
        df_filtered - Pandas DataFrame containing city data filtered by month and day
        df - Pandas Dataframe containing city data unfiltered
    """
    df = pd.read_csv(CITY_DATA[city])
    df_filtered = df
    df_filtered['Start Time'] = pd.to_datetime(df_filtered['Start Time'])
    df_filtered['Month'] = df_filtered['Start Time'].dt.month
    if month != 'all months':
        df_filtered = df_filtered[df_filtered['Month']== months_dict[month]]

    df_filtered['Day of week'] = df_filtered['Start Time'].dt.weekday
    if day != 'all days':
        df_filtered = df_filtered[df_filtered['Day of week']==weekday_dict[day]]

    return df, df_filtered


def time_stats(df_unfiltered,df,city,month,day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    df_unfiltered['Start Time'] = pd.to_datetime(df_unfiltered['Start Time'])
    df_unfiltered['Month'] = df_unfiltered['Start Time'].dt.month
    most_common_month_numeric = int(df_unfiltered['Month'].mode()[0])
    most_common_month_letters = list(months_dict.keys())[most_common_month_numeric-1]
    most_common_month_count = int(df_unfiltered[df_unfiltered['Month'] == most_common_month_numeric]['Month'].value_counts())
    print('The most common month in {}  is {} with a count of {} '.format(city,most_common_month_letters, most_common_month_count))

    # display the most common day of week
    df_unfiltered['Day of week'] = df_unfiltered['Start Time'] .dt.weekday
    most_common_weekday_numeric = df_unfiltered['Day of week'].mode()[0]
    most_common_weekday_letters = list(weekday_dict.keys())[most_common_weekday_numeric-1]
    most_common_weekday_count = df_unfiltered[df_unfiltered['Day of week'] == most_common_weekday_numeric]['Day of week'].value_counts()
    most_common_weekday_count = int(most_common_weekday_count)
    print('Most common day of week in {} in {} is {} with a count of {} '.format(city,month, most_common_weekday_letters, most_common_weekday_count))

    # display the most common start hour
    df['Start Hour'] = df['Start Time'] .dt.hour
    most_common_hour = df['Start Hour'].mode()[0]
    most_common_hour_count = df[df['Start Hour'] == most_common_hour]['Start Hour'].value_counts()
    most_common_hour_count = int(most_common_hour_count)
    print('Most common start hour in {} on {} in {} is {} with a count of {} '.format(city,day,month, most_common_hour, most_common_hour_count))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df,city,month,day):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('The most common start station in {} on {} in {} is {}'.format(city,day,month,most_common_start_station))

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('The most common end station in {} on {} in {} is {}'.format(city,day,month,most_common_end_station))

    # display most frequent combination of start station and end station trip
    most_common_combination = df.groupby(['Start Station'])['End Station'].value_counts().nlargest(1)
    print('The most common combination of start station and end station:\n {}'.format(str(most_common_combination)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df,city,day,month):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Travel Time'] = df['End Time'] - df['Start Time']
    total_travel_time = df['Travel Time'].sum()
    print('Total travel time in {} on {} in {} is {}'.format(city,day,month,total_travel_time))

    # display mean travel time
    mean_travel_time = df['Travel Time'].mean()
    print('Mean travel time in {} on {} in {} is {}'.format(city,day,month,mean_travel_time))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city,month,day):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('\nThe Breakdown of user types: \n {} '.format(str(df['User Type'].value_counts())))

    # Display counts of gender
    try:
        print('\nThe Breakdown of gender types: \n {} '.format(str(df['Gender'].value_counts())))
    except (KeyError):
        print('No gender data')
    # Display earliest, most recent, and most common year of birth

    try:
        print('\nThe most common year of birth in {} on {} in {} is {}'.format(city,day,month,int(df['Birth Year'].mode()[0])))
        print('Earliest year of birth in {} on {} in {} is {} '.format(city,day,month,int(df['Birth Year'].min())))
        print('The most recent year of birth in {} on {} in {} is {} '.format(city,day,month,int(df['Birth Year'].max())))
    except(KeyError):
        print('No year of birth data')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

'''display raw data after asking the user'''
def surf_raw_data(df):
    surf = ''
    while surf not in ['yes','no'] :
        surf = input('Would you like to surf the raw filtered data? please enter yes or no : ').lower().strip()
        if (surf == 'yes') :
            print(df.head())
            surf = int(0)
            surf_more = 'yes'
            while surf_more.lower().strip() == 'yes':
                surf_more = input('would you like to surf the next 5 rows of filtered raw data? Please enter yes or no?')
                surf = surf + 5
                print(df[surf:surf+5])
            break

def main():
    while True:
        city, month, day = get_filters()
        df_unfiltered,df = load_data(city, month, day)

        time_stats(df_unfiltered,df,city,month,day)
        input('Continue')
        station_stats(df,city,month,day)
        input('Continue')
        trip_duration_stats(df,city,day,month)
        input('Continue')
        user_stats(df,city,day,month)
        surf_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
