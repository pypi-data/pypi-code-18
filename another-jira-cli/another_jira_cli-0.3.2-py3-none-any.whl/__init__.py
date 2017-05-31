#!/usr/bin/env python

import click
import jira as jira_interface
from jira.exceptions import JIRAError

import stat
import json
import arrow
import os
import sys
import csv
import yaml
from datetime import date
import re
from functools import lru_cache


# ============================================================================
# VERSION
# ============================================================================

__version__ = "0.3.2"

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================


def get_cfg_file_path():
    user_home = os.environ["HOME"]
    return os.path.join(user_home, ".jira", "config")


def read_config():
    """
    Reads the configuration from the config file, usually $HOME/.jira/config

    :return: The configuration dict.
    """
    cfg_file_path = get_cfg_file_path()
    if not os.path.isfile(cfg_file_path):
        print("ERROR: Config file not found. Invoke the script with 'init'.")
        sys.exit(-1)
    return json.load(open(get_cfg_file_path(), "r", encoding='utf-8'))


def save_config(config):
    """
    Saves the configuration to the disk.

    :param config: The config dict object to save
    :return: None
    """
    cfg_file_path = get_cfg_file_path()
    cfg_file_dir = os.path.dirname(cfg_file_path)
    if not os.path.isdir(cfg_file_dir):
        perms_dir = stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR
        os.mkdir(cfg_file_dir)
        os.chmod(cfg_file_dir, perms_dir)
    perms_file = stat.S_IRUSR | stat.S_IWUSR
    with open(cfg_file_path, "w") as cfgfile:
        cfgfile.write(json.dumps(config))
    # always, just because we can :)
    os.chmod(cfg_file_path, perms_file)


def parse_date_str(date_str=None):
    """
    The date_str is interpreted as follows:

    * a string starting with m is always parsed as "m<number>" (e.g. m1, m3,
      etc.). it is then interpreted as <number> days before today, so "m1" is
      yesterday (minus 1), "m2" is the day before (minus 2), etc.

    * a string of length one or two is always parsed as a number, which is then
      interpreted as the nth day of the current month. so 1, 11, 12, etc. is the
      1st, 11th and 12th of the current month.

    * a string of length 4 is always parsed as MMDD

    * a string of length 8 is always parsed as YYYYMMDD

    * all other inputs result in an error and the program exiting.

    :param date_str: The date string to be parsed
    :return: An Arrow instance pointing to the parsed date
    """
    arr = arrow.now()
    if date_str is not None:
        if date_str[0] == "m":
            arr = arr.replace(days=-int(date_str[1:]))
        elif len(date_str) < 3:
            arr = arr.replace(day=int(date_str))
        elif len(date_str) == 4:
            arr = arr.replace(month=int(date_str[0:2]), day=int(date_str[2:]))
        elif len(date_str) == 8:
            arr = arr.replace(year=int(date_str[0:4]),
                              month=int(date_str[4:6]),
                              day=int(date_str[6:]))
        else:
            print("ERROR: Cannot parse date string '{}'!".format(date_str))
            sys.exit(-2)
    return arr


def parse_start_time_str(start):
    """
    Parses a string as HHMM and returns it as (HH, MM) tuple.

    :param start: The string to be parsed.
    :return: The parsed (int, int) tuple
    """
    if len(start) != 4:
        print("ERROR: start time *must* be in the form '1234'. Aborting.")
        sys.exit(-2)
    return int(start[0:2]), int(start[2:])


@lru_cache()
def get_jira():
    config = read_config()
    jobj = jira_interface.JIRA(config['jira_url'],
                               basic_auth=(config['username'],
                                           config['password']))
    return jobj


def get_tickets_logged_on_date(date:arrow.arrow.Arrow,
                               jira_obj:jira_interface.JIRA) -> list:
    """
    Uses the query 'worklogDate = "DATE" and worklogAuthor = currentUser()' to
    determine which tickets the user logged on a specific DATE.

    From the docs:

    jira.search_issues(jql_str, startAt=0, maxResults=50,
                       validate_query=True,
                       fields=None, expand=None, json_result=None)

    That should do it.

    :param date: The date as arrow object
    :param jira_obj: The JIRA object to use for querying
    :return: A list of tickets
    """
    date_str = date.format("YYYY-MM-DD")
    jql_query = 'worklogDate = "{}" and worklogAuthor = currentUser()'
    tickets_on_date = jira_obj.search_issues(jql_query.format(date_str))

    # this is not a list.
    return tickets_on_date


def add_worklog(jira, ticket_str, use_datetime, worklog, comment,
                no_output=False):
    config = read_config()
    if "aliases" in config and ticket_str in config["aliases"]:
        # we have an alias, use it.
        if not no_output:
            print("Resolving alias '{}' to ticket {}"
                  .format(ticket_str, config["aliases"][ticket_str]))
        ticket_obj = jira.issue(config["aliases"][ticket_str])
    else:
        ticket_obj = jira.issue(ticket_str)
    jira.add_worklog(ticket_obj,
                     started=use_datetime,
                     timeSpent=worklog,
                     comment=comment)


def parse_date_str_file(date_str_in=None):
    """
    get date string in a format of logwork on Jira
    :param: date_str_in: date in format 'YYYY-MM-DD HH:MM', if None then datetime.now
    :return: arrow.datetime format
    """
    if (date_str_in==None) or (date_str_in==''):
        arr = arrow.get(None).datetime
    else:
        try:
            arr = arrow.get(date_str_in)
            if arr.datetime.hour == 0:
                arr = arr.replace(hour=+9)
            arr = arr.replace(hours=-2).datetime
        except arrow.parser.ParserError as e:
            arr = arrow.get(None).datetime
            print("wrong date time, set to today")
    return arr


def log_csv(csv_file, jira, delimiter):
    """
    log work from csv file
    :param: csv_file:
                issue;date;log-time;comment
                ticket1;;'30m';comment1
                ticket2;2017-01-01 09:00;'1h 30m';comment2
    :param: jira: jira interface
    """
    with open(csv_file, "r", encoding='utf-8') as file:
        dict_lines = csv.DictReader(file, delimiter=delimiter)
        for num_row, row_in in enumerate(dict_lines, start=1):
            row = {key: value.strip() for key, value in row_in.items()}
            add_worklog(jira,
                        row['issue'], parse_date_str_file(row['date']),
                        row['log-time'], row['comment'])


def log_yaml(yaml_file, jira):
    """
    log work from yaml file
    :param: yaml_file:
                date1:  ! the default date is today
                    task1: ticket-1, 30m, 11:00, comment 1  ! ticket, log-time, started time, comment
                    task2: ticket-1, 1h 30m, comment 2    ! without started time, default 09:00
                    task3: ticket-2, 2h, 13:00   ! without comment, default 'no comment'
                date2:
                    date: 2017-01-01    ! add this if you want to define the date
                    task1: ticket-1, 1h, coment 3
    :param: jira: jira interface
    """
    f = open(yaml_file)
    data_map = yaml.safe_load(f)
    for key, line in data_map.items():
        parse_line = parse_yaml(line)
        add_worklog(jira,
                    parse_line['issue'], parse_date_str_file(parse_line['date']),
                    parse_line['log-time'], parse_line['comment'])


def parse_yaml(data):
    """
    parse yaml line
    :param data: lines read in from yaml
    :return: dict of task: {'issue': , 'date': , 'log-time': ,'comment': }
    """
    dict_out = {}
    daytime = date.today().__str__()
    if 'date' in data.keys():
        daytime = data['date'].__str__()
        data.pop('date')
    for key, detail in data.items():
        detail_list = [x.strip() for x in detail.split(',')]
        dict_out['date'] = daytime + ' ' + '09:00'
        t1 = re.findall(r'\d{2}:\d{2}', detail)
        if t1:
            dict_out['date']=daytime + ' ' + t1[0]
            detail_list.remove(t1[0])
        dict_out.update({'issue': detail_list[0],
                         'log-time': detail_list[1],
                         'comment': 'no comment'})
        if len(detail_list) > 2:
            dict_out.update({'comment': detail_list[2]})
    return dict_out


# ============================================================================
# COMMANDS START HERE
# ============================================================================


@click.group()
def cli():
    pass


@cli.command()
def version():
    print(__version__)


@cli.command()
@click.option("--jira-url", prompt=True,
              default=lambda: os.environ.get("JIRA_URL", ''))
@click.option("--username", prompt=True,
              default=lambda: os.environ.get("JIRA_USER", ''))
@click.option("--password", prompt=True,
              hide_input=True,
              default=lambda: os.environ.get("JIRA_PASSWORD", ''))
def init(**kwargs):
    save_config(kwargs)


@cli.command()
@click.argument("searchstring")
def search(searchstring):
    pass


@cli.command(name="cleanup-day")
@click.argument("date")
def cleanup_day(date):
    """
    Re-orders the work logs for a day.

    This means that it will re-sort all the logged time entries to follow one 
    after another, so that it looks nice in the JIRA calendar view.
    """
    arr = parse_date_str(date)
    jira = get_jira()
    tickets = get_tickets_logged_on_date(arr, jira)
    start_time = arrow.get(arr.format('YYYY-MM-DD')).replace(hours=+9)
    for ticket in tickets:
        for logticket in jira.worklogs(ticket.key):
            logticket.update({'started': start_time.__str__().replace('00+00:00', '00.000+0200')})
            start_time = start_time.replace(seconds=+int(logticket.timeSpentSeconds))


@cli.command(name="log-time")
@click.argument("ticket")
@click.argument("logdata", nargs=-1)
@click.option("--comment", default=None)
@click.option("--nono", is_flag=True,
              help="Don't actually log, just print the info")
def log_time(ticket, logdata, comment, nono):
    """
    This creates a work log entry for an issue. The general way of specifying
    the LOGDATA is:

        WORKLOG_STRING(1h) DATE(current day) START_TIME(0900)
    
    The values of the defaults are in brackets. You can specify the DATE using 
    several ways: "m1", "m3", ... means (m)inus 1 day, (m)inus 3 days, etc. So
    this is yesterday and three days ago. "1", "3" means the 1st or the 3rd of
    the current month, "0110" is the 10th of January this year, and "20150110" 
    is the same date in the year 2015.

    Examples (all examples will log on ticket IO-1234):

      - [...] IO-1234                    (log 1h today, starting at 0900)

      - [...] IO-1234 "2h 4m"            (log "2h 4m" today, starting at 0900)

      - [...] IO-1234 1.5h m3            (log 1.5h three days ago, ...)

      - [...] IO-1234 1.5h 12            (1.5h, at the 12th this month)

      - [...] IO-1234 1.5h 0112          (1.5h at the 12th of Jan)

      - [...] IO-1234 1.5h 20160112      (same, but 2016)

      - [...] IO-1234 1.5h 20160112 1000 (same, but work log starts at 1000)
        
    """
    # logdata must be: HOURS DATE START_TIME
    logdata_default = ("1h", None, "0900")
    use_worklog = logdata + logdata_default[len(logdata):]
    worklog, date, start = use_worklog
    arr = parse_date_str(date)
    use_hour, use_minute = parse_start_time_str(start)
    arr = arr.replace(hour=use_hour, minute=use_minute, second=0)
    use_datetime = arr.datetime
    print("DATE           :  {}".format(arr.to('Europe/Berlin').format()))
    print("WORKLOG STRING : '{}'".format(worklog))
    print("WORKLOG COMMENT: {}".format("'{}'".format(comment)
                                       if comment else '<empty>'))
    if nono:
        print("Stopping here. No log was performed.")
    else:
        jira = get_jira()
        add_worklog(jira, ticket, use_datetime, worklog, comment)


@cli.command(name="log-time-file")
@click.argument("file")
@click.option("-dl", "--delimiter", default=';',
              help="delimiter for csv file")
def log_fromfile(file, delimiter):
    jira = get_jira()
    if '.csv' in file:
        log_csv(file, jira, delimiter)
    elif '.yaml' in file:
        log_yaml(file, jira)


@cli.command()
@click.argument("alias_name")
@click.argument("ticket_id")
@click.option("--nocheck", is_flag=True,
              help="Don't try to check whether the ticket actually exists")
def alias(alias_name, ticket_id, nocheck=False):
    """
    Creates an alias for a certain ticket. That alias can be used to log time
    on instead of the ticket name.
    """
    config = read_config()
    try:
        if not nocheck:
            jira = get_jira()
            jira.issue(ticket_id)
        if "aliases" not in config:
            config["aliases"] = {}
        config["aliases"][alias_name] = ticket_id
        save_config(config)
        print("Alias '{}' -> '{}' created successfully."
              .format(alias_name, ticket_id))
    except JIRAError as e:
        print("JIRA ERROR: {}".format(e.text))


@cli.command()
@click.argument("alias_name")
def unalias(alias_name):
    """
    Removes a ticket alias.
    """
    config = read_config()
    if "aliases" not in config:
        print("No aliases defined.")
    elif alias_name not in config["aliases"]:
        print("No such alias: '{}'".format(alias_name))
    else:
        del config["aliases"][alias_name]
        save_config(config)
        print("Alias '{}' removed.".format(alias_name))


@cli.command(name="list-aliases")
def list_aliases():
    """
    Lists all ticket aliases.
    """
    config = read_config()
    if "aliases" not in config or len(config["aliases"]) == 0:
        print("No aliases defined.")
    else:
        max_alias_len = max(map(lambda x: len(x), config["aliases"].keys()))
        for a, t in sorted(config["aliases"].items(), key=lambda x: x[0]):
            print("{:>{width}} -> {}".format(a, t, width=max_alias_len))


@cli.command(name="clear-aliases")
def clear_aliases():
    """
    Removes all ticket aliases.
    """
    config = read_config()
    if "aliases" not in config or len(config["aliases"]) == 0:
        print("No aliases defined.")
    else:
        del config["aliases"]
        save_config(config)
        print("All aliases cleared.")


def console_entrypoint():
    pass


cli()
