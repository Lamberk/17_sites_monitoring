import argparse
import requests
import datetime

from urllib.parse import urlparse

from pythonwhois import get_whois
from pythonwhois.shared import WhoisException


QUANTITY_OF_DAYS = 30


def get_domain(url):
    return urlparse(url).netloc


def get_date_after_today(days_number):
    return datetime.datetime.today() + datetime.timedelta(days_number)


def load_urls4check(path):
    with open(path) as txt_file:
        return [line.strip() for line in txt_file]


def get_site_statuses(url):
    domain_name = get_domain(url)
    return {
        'response': get_server_response_status(url),
        'domain': get_domain_status(domain_name)
    }


def get_server_response_status(url):
    response = requests.get(url)
    return response.status_code == 200


def get_domain_status(domain_name):
    try:
        response = get_whois(domain_name)
    except WhoisException as e:
        print(e)
    else:
        date = get_date_after_today(QUANTITY_OF_DAYS)
        return response['expiration_date'][0] > date


def print_statuses(statuses):
    for status_type, status in statuses.items():
        status_str = 'OK' if status else 'FAIL'
        print(status_type, '{0}!'.format(status_str))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', help='Path to file', required=True)
    args = parser.parse_args()

    urls = load_urls4check(args.path)
    for url in urls:
        print('#'*80)
        print(url)
        status = get_site_statuses(url)
        print_statuses(status)
