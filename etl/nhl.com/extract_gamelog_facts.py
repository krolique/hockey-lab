# -*- coding: utf-8 -*-
"""
    Extract GameLog Facts
    ---------------------

    Generates a stream of NHL Gamelog facts

"""

from os import environ
from sys import stdout
from json import dumps
import sys

import requests
from bs4 import BeautifulSoup

from utils import latinize


#: the endpoint url used by the extractor function
ENDPOINT_URL = environ.get('ENDPOINT_URL',
                           'http://{team_name}.ice.nhl.com/club/'
                           'gamelog.htm?season={years}&gameType={game_type}')


#: defines the timeout in seconds the extractor function should spend
#: for the entire request
REQUEST_TIMEOUT = int(environ.get('REQUEST_TIMEOUT', 10))


def fetch_html(team_name, from_year, to_year, game_type,
               endpoint_url=ENDPOINT_URL, timeout=REQUEST_TIMEOUT):
    """ Returns game log data for a given team, game type and season

    :param team_name: short name of the team
    :type team_name: str
    :param from_year: beginning year for the season
    :type from_year: int
    :param to_year: ending year for the season
    :type to_year: int
    :param game_type: one of two values regular or playoffs
    :param game_type: str
    :param endpoint_url: the endpoint to fetch data from
    :type endpoint_url: str
    :param timeout: request timeout time in seconds
    :type timeout: int
    :returns: JSON from the
    :rtype: str
    """

    # the query string params on the NHL.com side accepts one of two
    # values 2 or 3 for game type. Where 2 means regular and 3 playoffs.
    # Since we're wrapping this knowledge the rest of the module
    # doesn't need to know about this translation.
    if game_type == 'regular':
        game_type = 2
    elif game_type == 'playoffs':
        game_type = 3
    else:
        raise RuntimeError(f'game type of {game_type} is not supported')

    years = f'{from_year}{to_year}'
    url = endpoint_url.format(team_name=team_name, years=years,
                              game_type=game_type)
    response = requests.get(url=url, timeout=timeout)
    response.raise_for_status()
    return response.text


def extract_title(table_row):
    """ Returns data table title text

    :param table_row: row object from the data table
    :type table_row: class
    :returns: cleaned up title text from table header row
    :rtype: str
    """

    title_txt = table_row.find(name='div').text
    title_txt = title_txt.replace('\n', '').replace('\t', '').strip()
    title_txt = title_txt.lower()
    return title_txt


def extract_col_name(table_row):
    """ Returns table column names

    :param table_row: row object from the data table
    :type table_row: class
    :return names of the columns in the table
    :rtype: list
    """

    data = []
    columns = table_row.findAll(name='td')
    for col in columns:
        value = latinize(col.text.strip())
        data.append(value)

    return data


def game_facts(html_text, from_year, to_year, game_type):
    """ Generates a sequence of game facts extracted from an HTML response

    :param html_text: raw HTML text returned from NHL.com site
    :type html_text: str
    :param from_year: beginning year for the season
    :type from_year: int
    :param to_year: ending year for the season
    :type to_year: int
    :param game_type: one of two values regular or playoffs
    :param game_type: str
    :returns: a sequence of game facts
    :rtype: generator
    """

    soup = BeautifulSoup(html_text, 'html.parser')
    table = soup.find(name='table', attrs={'class': 'data'})
    rows = table.findAll(name='tr')

    # The NHL.com static scraping is not an API call. What I've found from
    # observation of current implementation is they will do the following:
    #
    #   1.  if the team does not have playoff record they will return regular
    #       season game log
    #   2.  if the from year and to year data is not available they will
    #       return latest year game log
    #
    # these facts forces this module to perform a title check to ensure
    # we're not being lied to
    title = extract_title(table_row=rows[0])
    expected_prefix = f'{from_year}-{to_year} {game_type}'

    # the first 17 characters of the title currently follow this format
    # YYYY-YYYY regular/playoffs. By using this fact we can ensure the
    # resultant HTML table is the data we expected.
    if title[:17] != expected_prefix:
        # an exception would be more noticable if this piece stops working
        # correcly and an exception would make life harder on the consumer.
        # i'm not sure which is better yet.
        return

    keys = extract_col_name(table_row=rows[1])
    for row in rows[2:]:
        data = [value.text.replace('\n', '').strip()
                for value in row.findAll(name='td')]
        yield dict(zip(keys, data))


def generate_stream(team_name, from_year, to_year, game_type,
                    output_stream=None):
    """ Writes game log facts into the output stream

    :param team_name: short name of the team
    :type team_name: str
    :param from_year: beginning year for the season
    :type from_year: int
    :param to_year: ending year for the season
    :type to_year: int
    :param game_type: one of two values regular or playoffs
    :param game_type: str
    :param output_stream: the stream to which elements are emitted to
    :type output_stream: FileObject
    :rtype: None
    """

    if not output_stream:
        output_stream = stdout

    html = fetch_html(team_name=team_name, from_year=from_year,
                      to_year=to_year, game_type=game_type)

    for message in game_facts(html_text=html, from_year=from_year,
                              to_year=to_year, game_type=game_type):
        serialized = dumps(message)
        output_stream.write(f"{serialized}\n")


if __name__ == "__main__":

    try:
        TEAM_NAME = sys.argv[1]
    except IndexError:
        raise RuntimeError('missing team name parameter')

    try:
        FROM_YEAR = sys.argv[2]
    except IndexError:
        raise RuntimeError('missing from year parameter')

    try:
        TO_YEAR = sys.argv[3]
    except IndexError:
        raise RuntimeError('missing to year parameter')

    try:
        GAME_TYPE = sys.argv[4]
    except IndexError:
        raise RuntimeError('missing game type parameter')

    generate_stream(team_name=TEAM_NAME, from_year=FROM_YEAR,
                    to_year=TO_YEAR, game_type=GAME_TYPE)
