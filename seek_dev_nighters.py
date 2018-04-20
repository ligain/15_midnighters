import requests
import pytz
from datetime import datetime, time


API_URL = 'https://devman.org/api/challenges/solution_attempts'


def get_pagination_range(api_url):
    api_response = requests.get(api_url)

    if not api_response.ok:
        return
    json_response = api_response.json()
    start_page = json_response.get('page')
    end_page = json_response.get('number_of_pages')
    return start_page, end_page


def get_paginated_page(api_url, page_num, pagination_slug='page'):
    api_response = requests.get(
        api_url,
        params={pagination_slug: page_num}
    )

    if not api_response.ok:
        return []

    json_response = api_response.json()
    return json_response.get('records', [])


def load_attempts(api_url, start_page, end_page):
    for page in range(start_page, end_page):
        yield from get_paginated_page(api_url, page)


def is_midnighter(user_timestamp: float, user_timezone: str,
                  night_start=time(hour=0), night_end=time(hour=6)):

    user_tz = pytz.timezone(user_timezone)

    user_date_utc = datetime.utcfromtimestamp(
        user_timestamp).replace(tzinfo=pytz.utc)

    user_localized_date = user_date_utc.astimezone(user_tz)

    extracted_date = user_localized_date.date()

    localized_night_start = datetime.combine(
        extracted_date,
        night_start
    ).replace(tzinfo=user_tz)

    localized_night_end = datetime.combine(
        extracted_date,
        night_end
    ).replace(tzinfo=user_tz)

    if localized_night_start < user_localized_date < localized_night_end:
        return True
    return False


def get_midnighters(users_attempts):
    for attempt in users_attempts:
        user_timestamp = float(attempt.get('timestamp', 0.0))
        user_timezone = attempt.get('timezone', '')
        if user_timestamp and user_timezone and is_midnighter(
                user_timestamp, user_timezone):
            yield attempt.get('username', '')


def print_midnighters(midnighters):
    print('List of all midnighters on devman.com:')
    for midnighter in midnighters:
        print(midnighter)


if __name__ == '__main__':
    pagination_range = get_pagination_range(API_URL)

    if pagination_range is None:
        exit('Error loading json from the API endpoint')

    users_attempts = load_attempts(API_URL, *pagination_range)

    midnighters = set(get_midnighters(users_attempts))
    print_midnighters(midnighters)

