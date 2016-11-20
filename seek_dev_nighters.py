from pytz import timezone
from datetime import time, datetime
import requests


def load_attempts(pages=10):
    url = 'https://devman.org/api/challenges/solution_attempts'
    for page in range(1, pages + 1):
        params = {'page': page}
        response = requests.get(url, params=params).json()
        for record in response['records']:
            yield record


def is_midnighter(record):
    if record['timestamp']:
        user_time = datetime.fromtimestamp(record['timestamp'],
                                           timezone(record['timezone']))
        if time(00, 00) < user_time.time() < time(6, 00):
            return True


if __name__ == '__main__':
    midnighters = set()
    for record in load_attempts():
        if is_midnighter(record):
            midnighters.add(record['username'])
    print('\n'.join(midnighters))
