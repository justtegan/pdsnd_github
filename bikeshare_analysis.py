import time
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }

MONTHS = ['January','February','March','April','May','June']

DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = str(input("Enter city: "))
            if city not in CITY_DATA.keys():
                print(F"Not a valid city, please chose one of: {', '.join(CITY_DATA)}")
                continue
        except ValueError:
            print("Not a valid string")
            continue
        else:
            break
    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = str(input("Enter month: "))
            if month not in MONTHS and month != "All":
                print(F"Not a valid month, please chose one of: {', '.join(MONTHS)}, All")
                continue
        except ValueError:
            print("Not a valid string")
            continue
        else:
            break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = str(input("Enter day: "))
            if day not in DAYS and day != "All":
                print(F"Not a valid day, please chose one of: {', '.join(DAYS)}, All")
                continue
        except ValueError:
            print("Not a valid string")
            continue
        else:
            break

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
     # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city]) 
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'All':
        # use the index of the months list to get the corresponding int
        month = MONTHS.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
        
    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    # find the most common day of week
    popular_month = df['month'].mode()[0]

    print('Most Popular Month:', MONTHS[popular_month-1])

    # TO DO: display the most common day of week
    # find the most common day of week
    popular_day = df['day_of_week'].mode()[0]

    print('Most Popular Day Of Week:', popular_day)

    # TO DO: display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # find the most popular hour
    popular_hour = df['hour'].mode()[0]

    print('Most Popular Start Hour:', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most Popular Start Station:', popular_start_station)

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most Popular End Station:', popular_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    # Ref: https://stackoverflow.com/questions/40621802/sort-the-most-frequent-combinations-of-two-columns-in-descending-order
    popular_trips = df.groupby(['Start Station', 'End Station']).size().nlargest(5).reset_index(name='Trip Count')

    print(F"Top 5 Most Popular Trips:\n {popular_trips}")
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df["Trip Duration"].sum()
    print(F"Total Travel Time: {round(total_travel_time/60/60)} Hours")
    

    # TO DO: display mean travel time
    mean_travel_time = df["Trip Duration"].mean()
    print(F"Mean Travel Time: {round(mean_travel_time/60)} Minutes")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df["User Type"].value_counts()
    print(F"User Types:\n{user_types}\n")

    # TO DO: Display counts of gender
    gender_counts = df["Gender"].value_counts()
    print(F"Gender:\n{gender_counts}\n")

    # TO DO: Display earliest, most recent, and most common year of birth
    earliest_birth_year = df["Birth Year"].min()
    print(F"Earliest Birth Year: {earliest_birth_year}\n")
    latest_birth_year = df["Birth Year"].max()
    print(F"Most Recent Birth Year: {latest_birth_year}\n")
    common_birth_year = df["Birth Year"].mode()
    print(F"Common Birth Year: {common_birth_year}\n")
    
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
