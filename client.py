#!/usr/bin/env python
import re
from argparse import ArgumentParser

from TempThread import TempThread


def ip_checker(ip_address):
    pattern = re.compile(
        "^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.)"
        "{3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"
        "\:(?:(102[4-9]|10[3-9]\d|1[1-9]\d{2}|[2-9]\d{3}|[1-5]\d{4}"
        "|6[0-4]\d{3}|65[0-4]\d{2}|655[0-2]\d|6553[0-5]))$")
    if pattern.match(ip_address):
        return True
    return False


def domain_checker(domain):
    pattern = re.compile(
        "^([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}"
        "\:(?:(102[4-9]|10[3-9]\d|1[1-9]\d{2}|[2-9]\d{3}|[1-5]\d{4}"
        "|6[0-4]\d{3}|65[0-4]\d{2}|655[0-2]\d|6553[0-5]))$")
    if pattern.match(domain):
        return True
    return False


def parse_address(address_):
    try:
        address_ = address_.replace('http://', '')
        if domain_checker(address_) or ip_checker(address_):
            server_url_ = 'http://{}'.format(address_)
        else:
            server_url_ = 'http://127.0.0.1:8000'
    except AttributeError:
        server_url_ = 'http://127.0.0.1:8000'
    return server_url_


parser = ArgumentParser(
    description='Reads temperature from DS18B20 sensor, '
                'and sends it to server via it\'s API',
)
parser.add_argument('address', nargs='?')
args = parser.parse_args()
address = args.address
server_url = parse_address(address)

print('\n ******* Using {} as server address ******* \n'.format(server_url))

temp_thread = TempThread(server_url)
temp_thread.start()

raw_input('\n ******* Press ENTER key to stop and quit program ******* \n')

temp_thread.stop()
temp_thread.join()
