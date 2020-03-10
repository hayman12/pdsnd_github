import time
import pandas as pd
import numpy as np


CITY_DATA = {'Chicago': 'chicago.csv',
             'New York City': 'new_york_city.csv',
             'Washington': 'washington.csv'}


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
    while True:
        city = input(
            'Which city would you like to learn about? Chicago, New York City or Washington?\n ').lower().title()
        if city not in ('New York City', 'Washington', 'Chicago'):
            print('\nSorry, that is not a valid entry.\n')
            continue
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input(
            '\nWhich month would you like to see data for? I have data for January through June, or you can request \'all\':\n ').lower().title()
        if month not in ('January', 'February', 'March', 'April', 'June', 'All'):
            print('\nSorry, that is not a valid entry.')
            continue
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input(
            'Which day would you like to see data for? For the whole week, answer \'all\':\n ').lower().title()
        if day not in ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'All'):
            print('\nSorry, that is not a valid entry.')
            continue
        else:
            break

    print('-'*80)

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
    """  # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'All':
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'All':
        df['day'] = df['Start Time'].dt.weekday_name

       # filter by day of week to create the new dataframe
        df = df[df['day'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('The most popular month is:', popular_month)

    # display the most common day of week
    popular_day = df['day'].mode()[0]
    print('The most popular day of the week is:', popular_day)

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('The most popular start hour is:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    print('Most popular station to start a trip:', popular_start)

    # display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    print('Most popular station to end a trip:', popular_end)

    # display most frequent combination of start station and end station trip
    station_combos = df.groupby(['Start Station', 'End Station']).count()
    print('Most popular combination of stations to start and end a trip:',
          popular_start, 'and', popular_end)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    avg_trvl_time = df['Trip Duration'].sum()
    print('The total travel time was:', avg_trvl_time)

    # display mean travel time
    avg_trvl_time = df['Trip Duration'].mean()
    print('The average travel time was:', avg_trvl_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('User Types:\n', user_types.to_string())

    # Display counts of gender
    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts()
        print('Gender Counts:\n', gender.to_string())
    else:
        print('\nThere is no gender info available for Washington.')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_by = df['Birth Year'].min()
        print('\nThe earliest birth year is:', earliest_by)

        recent_by = df['Birth Year'].max()
        print('\nThe most recent birth year is:', recent_by)

        common_by = df['Birth Year'].mode()
        print('\nThe most common birth year is:', common_by.to_string())
    else:
        print('\nThere is no birth year data available for Washington')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():

    a = 0
    b = 5

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        more = input(
            'Would you like to view the first 5 lines of raw data, yes or no? ')

        if more.lower() == 'yes':
            while True:
                print(df.iloc[a:b])
                a = a + 5
                b = b + 5
                more_data = input(
                    'Would you like to view the next 5 lines of raw data, yes or no?')
                if more_data.lower() == 'no':
                    break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
