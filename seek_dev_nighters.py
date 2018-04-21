import requests
import pytz
from datetime import datetime, time


API_URL = 'https://devman.org/api/challenges/solution_attempts'


def get_paginated_page(api_url, page_num, pagination_slug='page'):
    api_response = requests.get(
        api_url,
        params={pagination_slug: page_num}
    )

    if not api_response.ok:
        return []

    json_response = api_response.json()
    return json_response.get('records', [])


def load_attempts(api_url, max_api_attempts=1000):
    page = 1
    failed_api_attempts = 0
    while failed_api_attempts < max_api_attempts:
        api_response = requests.get(api_url)

        if not api_response.ok:
            failed_api_attempts += 1
            continue

        json_response = api_response.json()
        yield from get_paginated_page(api_url, page)

        page += 1
        if page >= json_response.get('number_of_pages'):
            break


def is_midnighter(user_timestamp: float, user_timezone: str,
                  night_start_hour=0, night_end_hour=6):

    user_tz = pytz.timezone(user_timezone)

    user_date_utc = datetime.utcfromtimestamp(
        user_timestamp).replace(tzinfo=pytz.utc)

    user_localized_date = user_date_utc.astimezone(user_tz)
    if night_start_hour <= user_localized_date.hour <= night_end_hour:
        return True
    return False


def get_midnighters(users_attempts):
    for attempt in users_attempts:
        user_timestamp = attempt.get('timestamp')
        user_timezone = attempt.get('timezone')
        if user_timestamp and user_timezone and is_midnighter(
                user_timestamp, user_timezone):
            yield attempt.get('username', '')


def print_midnighters(midnighters):
    print('List of all midnighters on devman.com:')
    for midnighter in midnighters:
        print(midnighter)


if __name__ == '__main__':

    users_attempts = load_attempts(API_URL)

    midnighters = set(get_midnighters(users_attempts))
    print_midnighters(midnighters)
