#!/usr/bin/env python3
# This is a simple MQTT client publishing some system
# information to a broker. Uses Paho MQTT.
#
# Set environment var MQTT_BROKER as broker hostname or ip
#
# By: Visa Hannula

import json
import os
import socket
import sys
from sys import argv
from typing import Dict, Optional, Tuple

import paho.mqtt.publish as publish

MQTT_BROKER_HOST = os.environ.get('MQTT_BROKER')
main_topic = 'host'


"""Creates topics in a dict format for Paho client."""
def create_topics(info_dict: dict, start_str = '', topics=[]) -> list:
    curr_str = start_str
    for k, v in info_dict.items():
        if isinstance(v, dict):
            create_topics(v, f'{curr_str}/{k}', topics)
        else:
            topics.append({ 'topic':f'{curr_str}/{k}', 'payload': v })
    return topics

"""Get system info as dict. Calculates loadavg as percentage."""
def get_system_info(
        local_hostname: str,
        cpu_count: Optional[int],
        loadavg: Tuple[float, float, float]) -> Dict:

    loadavg = list(loadavg)
    cpu_count = 1 if cpu_count == None or cpu_count < 1 else cpu_count

    # Add percentage values using core count
    loadavg.extend([v / cpu_count * 100 for v in loadavg])
    loadavg_keys = ['loadavg1', 'loadavg5', 'loadavg15', 
                    'loadavg1percent', 'loadavg5percent', 'loadavg15percent']

    info_values = {
        local_hostname: {
            'cpu': {
                'count': cpu_count,
                'loadavg': dict(zip(loadavg_keys, loadavg))
            }
        }
    }

    return info_values


def print_topics(topics: dict):
    for topic in topics:
        print(f'{topic["topic"]} {topic["payload"]}')


class ConfigException(Exception):
    def __init__(self, msg):
        self.msg = msg
        print(f'Configuration error: {self.msg}')


# Publish
def pub_to_broker(topics):
    if not MQTT_BROKER_HOST:
        raise ConfigException('MQTT_BROKER not defined.')

    try:
        publish.multiple(topics, hostname=MQTT_BROKER_HOST, port=1883, 
                        keepalive=60, will=None, auth=None, tls=None)
    except OSError as os_err:
        print(f'OS Error: {os_err}')
        raise


def main(argv=[]):
    if len(argv) > 1 and argv[1] == '--help':
        print(f'Usage: {sys.argv[0]} [--topics]\n',
              f'   Without argument publish to broker.\n',
              f'   With argument only show topics (or --help).')
        return 0

    topics = create_topics(
        get_system_info(socket.gethostname(), os.cpu_count(), os.getloadavg()),
        start_str=f'{main_topic}')

    # any other argument will just print topics and values
    if len(argv) > 1 and not argv[1] == None:
        print(f'Broker: {MQTT_BROKER_HOST}')
        print(f'Printing {len(topics)} topics (no publish):')
        print_topics(topics)
        return 0
    # no arguments will publish
    else:
        print('Publishing to broker.')
        try:
            pub_to_broker(topics)
            return 0
        except (ConfigException, OSError):
            print(f'Could not publish.')


if __name__ == '__main__':
    sys.exit(main(sys.argv))
