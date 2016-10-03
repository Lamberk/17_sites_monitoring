import argparse
import requests
import datetime

from pythonwhois import get_whois


DAYS_NUMBER = 30


def get_date_after_today(days_number):
    return datetime.datetime.today() + datetime.timedelta(days_number)


def load_urls4check(path):
    with open(path, 'r') as txt_file:
        data = [line.strip() for line in txt_file]
        return data


def is_server_respond_with_200(url):
    response = requests.get('http://{}'.format(url))
    return (response.status_code == 200)


def get_domain_expiration_date(domain_name):
    response = get_whois(domain_name)
    date = get_date_after_today(DAYS_NUMBER)
    return (response['expiration_date'][0] > date)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', help='Path to file', required=True)
    args = parser.parse_args()
    urls = load_urls4check(args.path)
    for url in urls:
        print(
            url,
            'Ответил ли сервер 200?',
            is_server_respond_with_200(url),
            'Проплачен ли домен хотя бы на месяц вперед?',
            get_domain_expiration_date(url)
        )
