import requests
import pytz
from datetime import datetime


API_URL = 'https://devman.org/api/challenges/solution_attempts'


def load_attempts(api_url, max_api_attempts=5, pagination_slug='page'):
    page = 1
    failed_api_attempts = 0
    while failed_api_attempts < max_api_attempts:
        api_response = requests.get(
            api_url,
            params={pagination_slug: page}
        )

        if not api_response.ok:
            failed_api_attempts += 1
            continue

        json_data = api_response.json()
        if json_data.get('records'):
            yield from json_data.get('records')
        else:
            yield []

        page += 1
        if page >= json_data.get('number_of_pages'):
            break


def is_midnighter(user_timestamp: float, user_timezone: str,
                  night_start_hour=0, night_end_hour=6):

    user_tz = pytz.timezone(user_timezone)
    user_localized_date = datetime.fromtimestamp(user_timestamp, tz=user_tz)
    return night_start_hour <= user_localized_date.hour <= night_end_hour


def get_midnighters(users_attempts):
    for attempt in users_attempts:
        user_timestamp = attempt.get('timestamp')
        user_timezone = attempt.get('timezone')
        if user_timestamp and user_timezone and is_midnighter(
                user_timestamp, user_timezone):
            yield attempt.get('username', '')


def print_midnighters(midnighters):
    if midnighters:
        print('List of all midnighters on devman.com:')
        for midnighter in midnighters:
            print(midnighter)
    else:
        print('There are no midnighters on devman.com:')


if __name__ == '__main__':

    users_attempts = load_attempts(API_URL)

    midnighters = set(get_midnighters(users_attempts))
    print_midnighters(midnighters)
