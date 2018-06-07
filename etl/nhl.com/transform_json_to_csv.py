# -*- coding: utf-8 -*-
"""
    Transform JSON to CSV
    ---------------------

   Stream converter that changes message from JSON to CSV

"""

from sys import stdin, stdout
from csv import DictWriter
from json import loads


def process_stream(input_stream=None, output_stream=None):
    """ Processes the input stream

    :param input_stream: the stream from which to iterate input from
    :type input_stream: FileObject
    :param output_stream: the stream to which to write to
    :type output_stream: FileObject
    """
    if not input_stream:
        input_stream = stdin

    if not output_stream:
        output_stream = stdout

    input_str = input_stream.readline()
    header = loads(input_str)
    fields = header.get('fields')

    writer = DictWriter(output_stream, fieldnames=fields)
    writer.writeheader()
    for input_str in input_stream:
        message = loads(input_str)
        writer.writerow(message)


if __name__ == '__main__':
    process_stream()
