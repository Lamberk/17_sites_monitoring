import argparse
import requests
import datetime

from urllib.parse import urlparse

from pythonwhois import get_whois


QUANTITY_OF_DAYS = 30


def get_domain(url):
    return urlparse(url).netloc


def get_date_after_today(days_number):
    return datetime.datetime.today() + datetime.timedelta(days_number)


def load_urls4check(path):
    with open(path, 'r') as txt_file:
        urls = [line.strip() for line in txt_file]
        return urls


def get_site_status(url):
    error_log = []
    domain_name = get_domain(url)
    statuses = [get_server_response_status(url), get_domain_status(domain_name)]
    for status in statuses:
        if not status[0] == 'OK':
            error_log.append(status[1])

    if not error_log:
        status = 'OK'
    else:
        status = ('FAIL', error_log)
    return status


def get_server_response_status(url):
    response = requests.get(url)
    if response.status_code == 200:
        status = ('OK', 'Server response with 200')
    else:
        status = ('FAIL', 'Server response with {}'.format(response.status_code))
    return status


def get_domain_status(domain_name):
    response = get_whois(domain_name)
    date = get_date_after_today(QUANTITY_OF_DAYS)
    if response['expiration_date'][0] > date:
        status = ('OK', 'Domain doesn\'t expired')
    else:
        status = ('FAIL', 'Domain expired')
    return status

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', help='Path to file', required=True)
    args = parser.parse_args()
    urls = load_urls4check(args.path)
    for url in urls:
        status = get_site_status(url)
        print('{}............{}!'.format(url, status))
