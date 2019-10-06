import time
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Would you like to see data for: '
                 'Chicago, New York or Washington?\n').lower()
    while city not in ['chicago', 'new york', 'washington']:
        city = input(
            'Unknown City! Please choose from the following cities: '
            'Chicago, New York or Washington?\n').lower()

    # get user input for month (all, january, february, ... , june)
    month = input('Would you like to see data for: '
                  'January, February, March, April, May, June or All?\n').lower()
    while month not in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
        month = input(
            'Unknown Choice! Please choose from the following options: '
            'January, February, March, April, May, June or All?\n').lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input(
        'Would you like to see data for: '
        'Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or All?\n').lower()
    while day not in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
        day = input(
            'Unknown Choice! Please choose from the following options: '
            'Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or All?\n').lower()
    print('-' * 40)
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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month.lower() != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel.

    Args:
        df - DataFrame from load_data function filtered by month, city and day

    Returns:
        Statistics about:
            1. Most Frequent Month
            2. Most Frequent Day of Week
            3. Most Frequent Starting Hour
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month from the Start Time column to create a month column
    df['month'] = df['Start Time'].dt.month_name()

    # find the most common month (from January to June)
    popular_month = df['month'].mode()[0]

    # display the most common month
    print('Most Frequent Month:', popular_month)

    # extract day of week from the Start Time column to create a day of week column
    df['weekday'] = df['Start Time'].dt.weekday_name

    # find the most common weekday
    popular_weekday = df['weekday'].mode()[0]

    # display the most common day of week
    print('Most Frequent Day of Week:', popular_weekday)

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # find the most common hour (from 0 to 23)
    popular_hour = df['hour'].mode()[0]

    # display the most common start hour
    print('Most Frequent Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip.

    Args:
        df - DataFrame from load_data function filtered by month, city and day

    Returns:
        Statistics about:
            1. Most Frequent Start Station
            2. Most Frequent End Station
            3. Most Frequent Combined Station

    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most Frequent Start Station:', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most Frequent End Station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    # I used Knowledge Center as per the code review of my 1st submit
    df['Combined Station'] = df['Start Station'].map(str) + '&' + df['End Station']
    popular_combined_station = df['Combined Station'].mode()[0]
    print('Most Frequent Combined Station:', popular_combined_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = pd.to_timedelta(df['Trip Duration'].sum(), unit='s')
    print('Total Travel Time:', total_travel_time)

    # display mean travel time
    mean_travel_time = pd.to_timedelta(df['Trip Duration'].mean(), unit='s')
    print('Average Travel Time:', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(city, df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df.groupby('User Type').size()
    print(user_type)

    # Display counts of gender
    if city in ['chicago', 'new york']:
        gender = df.groupby('Gender').size()
        print(gender)

        # Display earliest, most recent, and most common year of birth
        earliest_birth_year = int(df['Birth Year'].min())
        most_recent_birth_year = int(df['Birth Year'].max())
        most_common_birth_year = int(df['Birth Year'].mode()[0])

        print('The Earliest Year of Birth: ', earliest_birth_year)
        print('The Most Recent Year of Birth: ', most_recent_birth_year)
        print('The Most Common Year of Birth: ', most_common_birth_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def data_sample(df):
    """
   Display samples of 5 rows on demand .

   Args:
       df - The Whole Pandas DataFrame
   Returns:
       df - Sample of 5 Rows from the whole Pandas DataFrame
   """
    demand = input('Would you like to see sample of raw data? Yes/No\n').lower()

    if demand == 'yes':
        print(df.sample(5))
        return data_sample(df)
    elif demand == 'no':
        return None
    else:
        print('Unknown Entry!')
        return data_sample(df)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(city, df)
        data_sample(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
