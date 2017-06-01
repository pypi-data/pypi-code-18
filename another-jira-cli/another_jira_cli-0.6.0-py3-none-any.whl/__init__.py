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
from functools import lru_cache, wraps


# ============================================================================
# VERSION
# ============================================================================


__version__ = "0.6.0"


# ============================================================================
# DECORATORS
# ============================================================================


def catch_jira_errors(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except JIRAError as e:
            print("JIRA ERROR: {}".format(e.text))
            sys.exit(-1)
    return inner


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

    * if None the current day is returned

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


def parse_date_str_file(date_str_in=None):
    """
    Let arrow parse the date_str_in. On any error return todays date at 09:00h.
    date_str_in should be in the format "YYYY-MM-DD HH:MM"

    :param: date_str_in: The date string to be parsed
    :return: date.datetime object
    """
    arr = arrow.get(None).datetime
    if not date_str_in:
        return arr
    try:
        arr = arrow.get(date_str_in)
        if arr.datetime.hour == 0:
            arr = arr.replace(hour=+9)
        arr = arr.replace(hours=-2).datetime
    except arrow.parser.ParserError as e:
        arr = arrow.get(None).datetime
        print("wrong date time, set to today")
    return arr


@lru_cache()
def get_jira():
    config = read_config()
    jobj = jira_interface.JIRA(config['jira_url'],
                               basic_auth=(config['username'],
                                           config['password']))
    return jobj


def get_tickets_logged_on_date(date:arrow.arrow.Arrow, user=None) -> list:
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
    jql_query = 'worklogDate = "{}" and worklogAuthor = {}'\
                .format(date_str, user if user else "currentUser()")
    jira_obj = get_jira()
    tickets_on_date = jira_obj.search_issues(jql_query)
    # now we have all tickets which contain worklogs by us on a date. now let's
    # get the worklogs.
    # this is not a list.
    return tickets_on_date


def get_worklogs_for_date_and_user(date, user=None):
    """
    Retrieves all work logs for a given user on a given day. Returns a
    list of the form: [[TICKET_OBJ, [WORKLOG0,...], ...]

    :param date: The date to search worklogs for
    :param user: The user to search worklogs for
    :return: The dict as described above
    """
    config = read_config()
    if not user:
        user = config["username"]
    jira = get_jira()
    logged_tickets = get_tickets_logged_on_date(date, user)
    worklogs = [(ticket, jira.worklogs(ticket.key))
                for ticket in logged_tickets]
    # this gives us all worklogs for all the tickets. now we need to ...
    # ... filter by author and date boundaries
    lb = date.floor('day')
    ub = date.ceil('day')
    final_logs = []
    for info_tuple in worklogs:
        wls = info_tuple[1]
        wls = filter(lambda x: x.author.name == user, wls)
        wls = list(filter(lambda x: lb < arrow.get(x.started) < ub, wls))
        if len(wls) > 0:
            final_logs.append((info_tuple[0], wls))
    # remove empty tickets :)
    return final_logs


def calculate_logged_time_for(tickets_and_logs):
    """
    Takes the output of get_worklogs_for_date_and_user and calculates the
    logged seconds for the day.

    :param tickets_and_logs: Return value of get_worklogs_for_date_and_user
    :return: The logged seconds
    """
    worklogs = []
    for info_tuple in tickets_and_logs:
        worklogs += info_tuple[1]
    return sum(map(lambda x: x.timeSpentSeconds, worklogs))


def get_hour_min(seconds):
    """
    Takes seconds and returns an (hours, minutes) tuple.
    :param seconds: The seconds to convert
    :return: The (hours, minutes) tuple
    """
    return (
        seconds // 3600,
        (seconds % 3600) // 60
    )


def check_for_alias(ticket_alias_str, no_output=False):
    """
    Checks whether the ticket string is an alias, if yes resolves it, if
    no returns it unchanged.

    :param ticket_alias_str: The potential ticket alias
    :param no_output: No output please
    :return: The input or the resolved alias
    """
    config = read_config()
    if "aliases" in config and ticket_alias_str in config["aliases"]:
        # we have an alias, use it.
        ticket = config["aliases"][ticket_alias_str]
        if not no_output:
            print("Resolving alias '{}' to ticket {}"
                  .format(ticket_alias_str, ticket))
        return ticket
    else:
        return ticket_alias_str


@lru_cache()
def get_ticket_object(ticket_str, no_output=False):
    """
    Returns a ticket object from a ticket key or a defined alias. The alias
    name has preference if somebody named an alias after a ticket.

    Will throw an exception if the alias or ticket can't be found.

    :param ticket_str: The ticket key or alias name.
    :param no_output: Whether to be silent while doing it.
    :return: A JIRA issue object
    """
    ticket_str = check_for_alias(ticket_str)
    jira = get_jira()
    ticket_obj = jira.issue(ticket_str)
    return ticket_obj


def add_worklog(ticket_str, use_datetime, worklog, comment,
                no_output=False):
    """
    Wrapper to add a timelog to JIRA. Mainly used to resolve a possible
    ticket alias in the process.

    :param ticket_str: The ticket identifier as string
    :param use_datetime: A datetime object with the start time and date
    :param worklog: The worklog time as used in JIRA (e.g. "1h 30m")
    :param comment: An optional comment
    :param no_output: If we should be silent
    :return:
    """
    jira = get_jira()
    ticket_obj = get_ticket_object(ticket_str, no_output)
    jira.add_worklog(ticket_obj,
                     started=use_datetime,
                     timeSpent=worklog,
                     comment=comment)


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
            add_worklog(row['issue'], parse_date_str_file(row['date']),
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
        add_worklog(parse_line['issue'], parse_date_str_file(parse_line['date']),
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


def perform_search(jql):
    try:
        jira = get_jira()
        results = jira.search_issues(jql)
        print("# {:<10} {:<20} {}".format("key", "author", "summary"))
        for result in results:
            sum = result.fields.summary
            aut = str(result.fields.reporter)
            use_sum = sum if len(sum) < 70 else sum[:67] + "..."
            use_aut = aut if len(aut) < 20 else aut[:17] + "..."
            print("{:<12} {:<20} {}".format(result.key, use_aut, use_sum))
    except JIRAError as e:
        print("Search string: {}".format(jql))
        print("ERROR: {}".format(e.text))


def search_wrapper(searchstring, save_as, just_save):
    if not just_save:
        perform_search(searchstring)
    if save_as:
        save_search(save_as, searchstring)


def save_search(search_alias, search_query):
    config = read_config()
    if not "saved_searches" in config:
        config["saved_searches"] = {}
    config["saved_searches"][search_alias] = search_query
    save_config(config)
    print("Search alias '{}' saved.".format(search_alias))


def print_table_from_dict(thedict, header=None):
    """
    Prints a formatted table from a dict.

    :param thedict: The dict to print as table
    :param header: Optional print a header for the columns. Must be a 2-tuple.
    :return:
    """
    max_col_len = max(map(lambda x: len(x), thedict.keys()))
    if header:
        max_col_len = max(len(header[0])+2, max_col_len)
        print("# {:<{width}}    {}"
              .format(header[0], header[1], width=max_col_len-2))
    for a, t in sorted(thedict.items(), key=lambda x: x[0]):
        print("{:<{width}}    {}".format(a, t, width=max_col_len))


# ============================================================================
# COMMANDS START HERE
# ============================================================================


@click.group()
def cli():
    pass


@cli.command()
def version():
    """
    Print the version and exits.
    """
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
    """
    Needs to be called one time to initialize URL, user and password.
    """
    save_config(kwargs)


@cli.command()
@click.argument("search-alias")
def lookup(search_alias):
    """
    Call a previously saved search.
    """
    config = read_config()
    if "saved_searches" not in config \
        or search_alias not in config["saved_searches"]:
        print("No such search alias: '{}'".format(search_alias))
        sys.exit(-1)
    perform_search(config["saved_searches"][search_alias])


@cli.command(name="remove-search")
@click.argument("search-alias")
def remove_search(search_alias):
    """
    Remove a search alias.
    """
    config = read_config()
    if "saved_searches" not in config \
        or search_alias not in config["saved_searches"]:
        print("No such search alias: '{}'".format(search_alias))
        sys.exit(-1)
    del config["saved_searches"][search_alias]
    save_config(config)
    print("Saved search '{}' removed.".format(search_alias))


@cli.command(name="list-searches")
def list_searches():
    """
    List all saved searches.
    """
    config = read_config()
    if "saved_searches" not in config:
        print("No saved searches.")
        sys.exit(-1)
    print_table_from_dict(config["saved_searches"],
                          header=("alias", "search query"))


@cli.command(name="clear-searches")
def clear_searches():
    """
    Delete all saved searches.
    """
    config = read_config()
    if "saved_searches" not in config:
        print("No saved searches.")
        sys.exit(-1)
    del config["saved_searches"]
    save_config(config)
    print("All saved searches cleared.")


@cli.command()
@click.argument("searchstring", nargs=-1)
@click.option("--save-as", default=None)
@click.option("--just-save", is_flag=True)
def search(searchstring, save_as, just_save):
    """
    Search for header or summary text.

    If you specify --save-as, the query is executed and - on success - saved
    as a search alias which you recall using the 'lookup' command later.

    If you additionally specify --just-save, the search is just saved as alias
    but not executed ('just saved', right? :).
    """
    lookup = " ".join(searchstring)
    lookup = "summary ~ \"{lup}\" OR description ~\"{lup}\"".format(lup=lookup)
    search_wrapper(lookup, save_as, just_save)


@cli.command()
@click.argument("jql_string", nargs=-1)
@click.option("--save-as", default=None)
@click.option("--just-save", is_flag=True)
def jql(jql_string, save_as, just_save):
    """
    Search for tickets using JQL.

    If you specify --save-as, the query is executed and - on success - saved
    as a search alias which you recall using the 'lookup' command later.

    If you additionally specify --just-save, the search is just saved as alias
    but not executed ('just saved', right? :).
    """
    lookup = " ".join(jql_string)
    search_wrapper(lookup, save_as, just_save)


@cli.command(name="cleanup-day")
@click.argument("date")
@click.option("--day-start", default="0900",
              help="When the first worklog should start. "
                   "Format must be HHMM.")
def cleanup_day(date, day_start):
    """
    Arrange the worklogs nicely for a given day.

    This means that it will re-sort all the logged time entries to follow one 
    after another, so that it looks nice in the JIRA calendar view.

    The original order is *tried* to be preserved, if the logs start at the
    exact same moment the ticket key is used as second indicator, then the
    worklog duration (descending).
    """
    date_obj = parse_date_str(date)
    start_h, start_m = parse_start_time_str(day_start)
    start_time = date_obj.floor('day').replace(hour=start_h, minute=start_m)
    tickets_and_logs = get_worklogs_for_dat1e_and_user(date_obj)
    # [(WORKLOG, TICKET), ...]
    tuples = [(v, sl[0]) for sl in tickets_and_logs for v in sl[1]]
    # sort by started date, then ticket key
    sortfunc = lambda x: x[0].started + x[1].key + \
                         "{:08d}".format(1000000-x[0].timeSpentSeconds)
    tuples = sorted(tuples, key=sortfunc)
    for wlog, ticket in tuples:
        next_time = start_time.replace(seconds=+int(wlog.timeSpentSeconds))
        print("{:<5} - {:<5}:  {:<10}  {}".format(
            start_time.format("HH:MM"), next_time.format("HH:MM"),
            ticket.key,
            wlog.comment if hasattr(wlog, "comment") and wlog.comment
                else "<no comment given>"
        ))
        wlog.update({'started': start_time.format("YYYY-MM-DDTHH:MM:SS.SSSZ")})
        start_time = next_time


@cli.command(name="log-time")
@click.argument("ticket")
@click.argument("logdata", nargs=-1)
@click.option("--comment", default=None)
@click.option("--nono", is_flag=True,
              help="Don't actually log, just print the info")
def log_time(ticket, logdata, comment, nono):
    """
    Create a work log entry in a ticket.

    The general way of specifying the LOGDATA is:

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
    # TODO - remove default timezone!!
    print("DATE           :  {}".format(arr.to('Europe/Berlin').format()))
    print("WORKLOG STRING : '{}'".format(worklog))
    print("WORKLOG COMMENT: {}".format("'{}'".format(comment)
                                       if comment else '<empty>'))
    if nono:
        print("Stopping here. No log was performed.")
    else:
        add_worklog(ticket, use_datetime, worklog, comment)


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
@click.argument("ticket_id")
@click.argument("alias_name")
@click.option("--nocheck", is_flag=True,
              help="Don't try to check whether the ticket actually exists")
@catch_jira_errors
def alias(ticket_id, alias_name, nocheck=False):
    """
    Create an alias name for a ticket.

    That alias can be used to log time on instead of the ticket name.
    """
    config = read_config()
    if not nocheck:
        jira = get_jira()
        jira.issue(ticket_id)
    if "aliases" not in config:
        config["aliases"] = {}
    config["aliases"][alias_name] = ticket_id
    save_config(config)
    print("Alias '{}' -> '{}' created successfully."
          .format(alias_name, ticket_id))


@cli.command()
@click.argument("alias_name")
def unalias(alias_name):
    """
    Remove a ticket alias.
    """
    config = read_config()
    if "aliases" not in config or alias_name not in config["aliases"]:
        print("No such alias: '{}'".format(alias_name))
    else:
        del config["aliases"][alias_name]
        save_config(config)
        print("Alias '{}' removed.".format(alias_name))


@cli.command(name="list-aliases")
def list_aliases():
    """
    List all ticket aliases.
    """
    config = read_config()
    if "aliases" not in config or len(config["aliases"]) == 0:
        print("No aliases defined.")
    else:
        print_table_from_dict(config["aliases"])


@cli.command(name="clear-aliases")
def clear_aliases():
    """
    Remove ALL ticket aliases.
    """
    config = read_config()
    if "aliases" not in config or len(config["aliases"]) == 0:
        print("No aliases defined.")
    else:
        del config["aliases"]
        save_config(config)
        print("All aliases cleared.")


@cli.command(name="fill-day")
@click.argument("date", default=None)
@click.option("--comment", default=None,
              help="Optional worklog comment")
@click.option("--day-hours", default=8.0)
@click.option("--day-start", default="0900",
              help="The start time of the day, format HHMM")
@click.option("--default", default=None,
              help="Specify a different default ticket")
@click.option("--re-init", is_flag=True,
              help="Re-enter the default ticket")
def fill_day(date, comment, day_hours, day_start, default, re_init):
    """
    "Fill" a day with a worklog.

    This command uses a 'default' ticket to log work on. It checks how much work
    was already logged on a given day, and then creates a worklog which uses the
    remaining available time.

    You can specify how long a day is FOR ONE EXECUTION using the
    --day-hours parameter, which takes a float argument (--day-hours 8.5). The
    default (which can't be changed right now) is 8.0.

    You can also specify a different default ticket to use FOR ONE EXECUTION
    using the --default option.

    If the day is not at all filled, the log entry will start at 09:00h, which
    you can adjust by using the --day-start option (which needs to be formatted
    HHMM).

    If 'date' is not given, it uses the present day.
    """
    start_h, start_m = parse_start_time_str(day_start)
    start_time = parse_date_str(date).floor('day')\
                                     .replace(hour=start_h, minute=start_m)
    config = read_config()
    if "fill_day" not in config or re_init:
        print("Enter default ticket to use (may be an alias): ", end="")
        default_ticket_str = input()
        # just try to see if it exists
        get_ticket_object(default_ticket_str)
        config["fill_day"] = {'default_ticket': default_ticket_str}
        save_config(config)
    else:
        default_ticket_str = config["fill_day"]["default_ticket"] \
                             if not default \
                             else default
    ticket_and_logs = get_worklogs_for_date_and_user(start_time)
    logged_work_secs = calculate_logged_time_for(ticket_and_logs)
    # calculate log metadata
    available_secs = day_hours * 60 * 60 - logged_work_secs
    in_hours, in_mints = get_hour_min(available_secs)
    # calculate latest starting point
    just_worklogs = [v for sublist in ticket_and_logs for v in sublist[1]]
    if len(just_worklogs) > 0:
        calculated_start_time = max([arrow.get(wl.started)
                                          .replace(seconds=wl.timeSpentSeconds)
                                     for wl in just_worklogs])
        if calculated_start_time < start_time.ceil('day'):
            # if logging was shit we could be in "tomorrow" already
            start_time = calculated_start_time
    # sanity checks
    if available_secs <= 60:
        print("You have already {}h {}m logged, not filling up."
              .format(*get_hour_min(logged_work_secs)))
    else:
        log_string = "{}h {}m".format(in_hours, in_mints)
        print("Adding {} to reach {} hours on {}."
              .format(log_string, day_hours, start_time.format("MMM Do")))
        comment = "[FUP] " + comment if comment else "[FUP]"
        add_worklog(default_ticket_str, start_time, log_string, comment)
        print("Logged {} on ticket {}."
              .format(log_string, default_ticket_str))


@cli.command(name="list-worklogs")
@click.argument("date", default=None)
def list_worklogs(date):
    """
    List all logs for a given day.
    """
    date_obj = parse_date_str(date)
    tickets_and_logs = get_worklogs_for_date_and_user(date_obj)
    logged_work_secs = calculate_logged_time_for(tickets_and_logs)
    # create a list like [(log_entry, ticket_obj), ...]
    tuples = [(v, sl[0]) for sl in tickets_and_logs for v in sl[1]]
    for log, ticket in sorted(tuples, key=lambda x: x[0].started):
        t_start = arrow.get(log.started).strftime("%H:%M")
        t_hrs, t_min = get_hour_min(log.timeSpentSeconds)
        cmt = log.comment \
            if hasattr(log, "comment") and log.comment \
            else "<no comment entered>"
        print("{:<8} {:<8} {:<8}  {:>2}h {:>2}m   {}"
              .format(log.id, ticket.key, t_start, t_hrs, t_min, cmt))
    print("\nSUM: {}h {}m"
          .format(logged_work_secs // 3600, (logged_work_secs%3600) // 60))


@cli.command(name="list-work")
@click.argument("date", default=None)
def list_work(date):
    """
    List on which tickets you worked how long on a given day.
    """
    date_obj = parse_date_str(date)
    tickets_and_logs = get_worklogs_for_date_and_user(date_obj)
    # create a list like [(log_entry, ticket_obj), ...]
    calced_times = [(t, sum([x.timeSpentSeconds for x in logs]))
                    for t, logs in tickets_and_logs]
    sum_time = sum([x[1] for x in calced_times])
    for ticket, seconds in sorted(calced_times, key=lambda x: x[0].key):
        use_time = "{}h {}m".format(*get_hour_min(seconds))
        use_sum = ticket.fields.summary
        if len(use_sum) > 70:
            use_sum = use_sum[:67] + "..."
        print("{:<10} {:<8}  {}".format(ticket.key, use_time, use_sum))
    print("\nSUM: {}h {}m".format(*get_hour_min(sum_time)))


@cli.command(name="delete-worklog")
@click.argument("ticket-id")
@click.argument("worklog-id")
@catch_jira_errors
def delete_worklog(ticket_id, worklog_id):
    """
    Delete a worklog entry by ID.

    Unfortunately you really need the ticket ID for the API it seems.
    """
    jira = get_jira()
    jira.worklog(check_for_alias(ticket_id), worklog_id).delete()


def console_entrypoint():
    pass


cli()
