from pytz import timezone
from datetime import time
from datetime import datetime as DT
import requests


def load_attempts():
    pages = 1
    url = 'https://devman.org/api/challenges/solution_attempts'
    for page in range(1, pages + 1):
        params = {'page': page}
        response = requests.get(url, params=params).json()
        for record in response['records']:
            yield record


def get_midnighters(record):
    moscow_tz = timezone('Europe/Moscow')
    user_tz = timezone(record['timezone'])
    if record['timestamp']:
        user_dt = user_tz.localize(DT.fromtimestamp(record['timestamp']))
        adj_user_dt = user_dt.astimezone(moscow_tz)
        user_time = time(adj_user_dt.hour, adj_user_dt.minute)
        if time(00, 00) < user_time < time(6, 00):
            return record['username']


if __name__ == '__main__':
    owls = []
    for record in load_attempts():
        owl = get_midnighters(record)
        if owl:
            owls.append(owl)
    print('\n'.join(owls))
