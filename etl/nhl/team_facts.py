# -*- coding: utf-8 -*-
"""
    Fact Stream
    -----------

    Generates a stream of NHL team facts

"""

from os import environ
from sys import stdout
from json import dumps

import requests


#: the endpoint url used by the extractor function
ENDPOINT_URL = environ.get('ENDPOINT_URL',
                           'https://statsapi.web.nhl.com/api/v1/teams')


#: defines the timeout in seconds the extractor function should spend
#: for the entire request
REQUEST_TIMEOUT = int(environ.get('REQUEST_TIMEOUT', 10))


def fetch_json(endpoint_url=ENDPOINT_URL, timeout=REQUEST_TIMEOUT):
    """ Returns JSON payload from endpoint response

    :param endpoint_url: the endpoint to fetch data from
    :type endpoint_url: str
    :param timeout: request timeout time in seconds
    :type timeout: int
    :returns: JSON from the
    :rtype: dict
    """

    response = requests.get(url=endpoint_url, timeout=timeout)
    response.raise_for_status()
    return response.json()


def generate_stream(payload_key='teams', output_stream=None):
    """ Emits payload elements to the output stream

    :param payload_key: name of the JSON property which contains the
                        collections of elements
    :type payload_key: str
    :param output_stream: the stream to which elements are emitted to
    :type output_stream: FileObject
    :rtype: None
    """

    if not output_stream:
        output_stream = stdout

    payload = fetch_json()
    for element in payload.get(payload_key):
        serialized = dumps(element)
        output_stream.write("{serialized}\n".format(serialized=serialized))


if __name__ == "__main__":
    generate_stream()
