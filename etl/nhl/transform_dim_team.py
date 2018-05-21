# -*- coding: utf-8 -*-
"""
    Transform Dim Team
    ------------------

    Transforms team fact into a dim_team

"""

from json import dumps, loads
from sys import stdout, stdin

from transliterate import translit, detect_language

#: defines entity propertie names
ENTITY_KEYS = ['full_name', 'short_name', 'abbreviation', 'location',
               'division', 'conference', 'first_year_of_play']


def translit_to_latin(value):
    """ Replaces UTF-8 characters to their latin equvalents

    :param value: the string to transliterate
    :type value: str
    :returns: transliterated string
    :rtype: str
    """

    # when this library function fails to detect a language
    # there is nothing to transliterate
    if not detect_language(value):
        return value
    # using the reversed param in the function enables the function to
    # substitute UTF-8 to latin
    return translit(value, reversed=True)


def transform(message):
    """ Transforms an api message into a dim team message

    :param message: an api response element
    :type message: dict
    :returns: transformed message object
    :rtype: dict
    """

    return {
        'full_name': translit_to_latin(value=message.get('name')),
        'short_name': message.get('shortName'),
        'team_name': message.get('teamName'),
        'abbreviation': message.get('abbreviation'),
        'location': message.get('locationName'),
        'division': message.get('division').get('name'),
        'conference': message.get('conference').get('name'),
        'first_year_of_play': message.get('firstYearOfPlay')
    }


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

    output_stream.write('{"type": "dim_team"}\n')
    output_stream.write(f'{ENTITY_KEYS}\n')
    for input_str in input_stream:
        message = loads(input_str)
        transformed = transform(message=message)
        serialized = dumps(transformed)
        output_stream.write(f'{serialized}\n')


if __name__ == '__main__':
    process_stream()
