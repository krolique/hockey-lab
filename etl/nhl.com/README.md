# NHL.com
This component enables scraping of the NHL.com API.


## Design
The general design is to avoid the tendency to write everything with the
assumption the data is clean, doesn't change and the processing steps are
not reversible. Data always changes, contract with external API change and
we reverse decisions all the time. Debugging an ETL job with these flaws is
painful and tends to discourage development.

The design here embraces change in all directions by refusing to write ETL
components int library functions or importable modules. These leads to
monoliths. Design here embraces streams and every steps is either generating
a stream, mutating a stream or saving output from a stream. The only way to
share state of data is by reading/writing to and from a stream.

Example of an ETL process for generating dimensional division facts to
standard output:

```bash
    $ python facts_team.py | python transform_dim_division. py
    {"type": "dim_division"}
    ['name']
    {"name": "Central"}
    {"name": "Pacific"}
    {"name": "Atlantic"}
    {"name": "Metropolitan"}
```

However it should be noted the end result of an ETL process is not always a
collection of pipes created here. For instance if you wish to filter a
stream based on some token. Don't write a new local pipe. Utilize the Linux
OS by using grep. Since grep works on STDIN and emits to STDOU

Example:

```bash
    $ python team_facts.py | grep -i central
    {
        "id": 16,
        "name": "Chicago Blackhawks",
        ...
    }
```

Sections below define each component more precisely and specify the contract
they must meet in order to ensure they can be integrated into the overall
design of the system.

### Facts 
A module that streams/emits facts. Generally speaking this is a wrapper
around the API endpoints capable of returning a payload.

The contract that must be meet by the stream: 
- Each message in the stream **MUST** be JSON realizable string
- Each row must end in a new line character
- Whenever possible the fact module should never attempt to alter the
original format. The output should be raw data from the API.
- Each message in the stream must end with a new line character

Example output:

```bash
    $ python team_facts.py
    {
        "id": 53,
        "teamName": "Arizona Coyotes",
        ...
    }
    {
        "id": 54,
        "teamName": "Vegas Golden Knights",
        ...
    }
```

### Transformer
A module that performs work on each message in the stream. Generally this is
where you will format the data into a shape more suitable for database domain
or clean the incoming data for consistency. Additionally is is possible to
convert from one format to another. Type transformers are really consumer
of the Data transformers or rather the should be joined together to
form the final product of an ET (minus L).

#### Data Transformer
A module that works on a stream of facts by transforming each element into
a data shape that closely resembles final models stored in database or 
in a usable state by other components in the system.

The contract that must be meet by the transformer:
- Emit the name of the message type as the first item in the stream
- Emit a list of message property names as the second item in the stream
- Emit N number of messages
- Each message of the stream **MUST** be JSON realizable string
- Each message in the stream must end with a new line character

Example output:
``` bash
    $ python team_facts.py |  python transform_dim_teams.py
    {"type": "dim_team"}
    ['id', 'name', .....]
    {
        "id": 53, 
        "name": "Arizona Coyotes", 
        ....
    }
    {
        "id": 54, 
        "name": "Vegas Golden Knights", 
        ...
    }
    ...
```

### TYPE Transformers

