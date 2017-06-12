"""Code for tagging date expressions in text."""


# ---- DEPENDENCIES ---- #


import re
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil.easter import easter


# ---- CONSTANTS ---- #

# lots of option group nesting used to match complex possibilites with a single regex,
# NOT  intended to be used for separation of components from matches.

# Predefined option groups.
NUMBERS = ("(^a(?=\s)|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
           "thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|"
           "forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand)")
HOLIDAY = ("(new(\s)?year(\')?s((\s)?eve)?|nye|cinco(\s)?de(\s)?mayo|mother(\')?s(\s)?day|"
           "valentine(\')?s((\s)?day)?|st(\s)?patrick(\')?s((\s)?day)?|st(\s)?patty(\')?s|"
           "st(\s)?paddy(\')?s|mardi(\s)?gras|fat(\s)?tuesday|shrove(\s)?tuesday|easter)")
WEEK_DAY = "(mon(day)?|tue(s)?(day)?|wed(nesday)?|thur(sday)?|fri(day)?|sat(urday)?|sun(day)?)"
MONTH = ("(jan(uary)?|feb(ruary)?|mar(ch)?|apr(il)?|may|jun(e)?|jul(y)?|aug(ust)?|september|sep(t)?|"
         "oct(ober)?|nov(ember)?|dec(ember)?)")
DMY = "(year|day|week|month)"
REL_DAY = "(today|yesterday|tomorrow|tonight|tonite)"
EXP1 = "(before|after|earlier|later|ago)"
EXP2 = "(this|next|last)"

# raw combined regexes
NUMBER_DAY_RELATIVE = "((\d+|(" + NUMBERS + "[-\s]?)+) " + DMY + "s? " + EXP1 + ")"
RELATIVE_DMY = "(" + EXP2 + " (" + DMY + "|" + WEEK_DAY + "|" + MONTH + "))"
RELATIVE_DAY = "(" + REL_DAY + ")"
ISO = "(((\d{4}|\d{2}|\d{1})[/-](\d{4}|\d{2}|\d{1})[/-](\d{4}|\d{2}|\d{1})(?: \d+:\d+:\d+)?))"
YEAR = "(((?<=\s)\d{4}|^\d{4}))([\s.,!]|$)"  # need punct/space at end of year
DAY_MONTH = "\s+((\d{1,2}[/-]\d{1,2}))([\s.,!]|$)"  # need punct/space at beginning/end
MONTH_DAY = '((' + MONTH + ')' + "\s\d{1,2})"
WEEKDAY_ONLY = '\s+((every\s+)?' + WEEK_DAY + '(\s+night)?)([\s.,!]|$)'
HOLIDAY_ONLY = '\s+(' + HOLIDAY + ')[\!\,\.\s+]'
RECURRING_DAILY = '((every day|everyday|every night))'
TODAY = '((this morning|this afternoon|this evening|last day))'

# times
AM_PM = "((\s|^)(\d{1,2})(:\d{2})?(\s)?(am?|pm?)([\s.,!]|$))"
NO_AM_PM = "((\s|^)(as of|until|around|at|by|from)( about| around| approx(\.)?(imately)?)?(\s)(\d{1,2})(:\d{1,2})?([\s.,!]|$))"
TIME_RANGES = "((\s|^)([1-9]|1[0-2])(\s?(am?|pm?))?(\s?-\s?)([1-9]|1[0-2])(\s?(am?|pm?))?([\s.,!]|$))"


# complied regexes
# five days ago etc...
REG1 = re.compile(NUMBER_DAY_RELATIVE, re.IGNORECASE)
# this tuesday etc...
REG2 = re.compile(RELATIVE_DMY, re.IGNORECASE)
# today tomorrow etc.
REG3 = re.compile(RELATIVE_DAY, re.IGNORECASE)
# iso date format
REG4 = re.compile(ISO)
# year only
REG5 = re.compile(YEAR)
# day then month
REG6 = re.compile(DAY_MONTH)
# written month numeric day
REG7 = re.compile(MONTH_DAY, re.IGNORECASE)
# just week day - possibly recurring
REG8 = re.compile(WEEKDAY_ONLY, re.IGNORECASE)
# just holiday
REG9 = re.compile(HOLIDAY_ONLY, re.IGNORECASE)
# recurring daily
REG10 = re.compile(RECURRING_DAILY, re.IGNORECASE)
# today
REG11 = re.compile(TODAY, re.IGNORECASE)
# time with am/pm
REG12 = re.compile(AM_PM, re.IGNORECASE)
# time without am/pm
REG13 = re.compile(NO_AM_PM, re.IGNORECASE)
# time range
REG14 = re.compile(TIME_RANGES, re.IGNORECASE)


# Hash function for week days to simplify the grounding task.
# [Mon..Sun] -> [0..6]
HASH_WEEKDAYS = {
    'monday': 0,
    'tuesday': 1,
    'tueday': 1,
    'wednesday': 2,
    'thursday': 3,
    'friday': 4,
    'saturday': 5,
    'sunday': 6,
    'mon': 0,
    'tue': 1,
    'tues': 1,
    'wed': 2,
    'thur': 3,
    'fri': 4,
    'sat': 5,
    'sun': 6}

# Hash function for months to simplify the grounding task.
# [Jan..Dec] -> [1..12]
HASH_MONTHS = {
    'january': 1,
    'february': 2,
    'march': 3,
    'april': 4,
    'may': 5,
    'june': 6,
    'july': 7,
    'august': 8,
    'september': 9,
    'october': 10,
    'november': 11,
    'december': 12,
    'jan': 1,
    'feb': 2,
    'mar': 3,
    'apr': 4,
    'may': 5,
    'jun': 6,
    'jul': 7,
    'aug': 8,
    'sep': 9,
    'sept': 9,
    'oct': 10,
    'nov': 11,
    'dec': 12}


# ---- HELPER FUNCTIONS ---- #


def split_hour_minute(time):
    """Split hour/minute into components."""
    stripped = time.strip().rstrip('?:!.,;')
    hourminute = stripped.split(':')
    if len(hourminute) > 1:
        hour = int(hourminute[0])
        minute = int(hourminute[1])
    else:
        hour = int(hourminute[0])
        minute = 0
    return hour, minute


def split_am_pm(time):
    """Separate time from am/pm if present."""
    split_am = re.split(r'a', time, flags=re.IGNORECASE)
    split_pm = re.split(r'p', time, flags=re.IGNORECASE)
    # three cases: 1. Letter "a" present, 2. letter "p" present, 3. neither present.
    # If 1, use am, if 2 use pm, otherwise use default
    if len(split_am) > 1:
        time = split_am[0].strip()
        am_pm = "am"
    elif len(split_pm) > 1:
        time = split_pm[0].strip()
        am_pm = "pm"
    else:
        time = split_pm[0].strip()
        am_pm = ""  # returning empty string here is key for subsequent logic
    return time, am_pm


def update_date_with_time(date, time, base_date):
    """Update a <DATE> datetime with a <TIME> datetime."""
    # this will only be true if day was updated in time search.
    if time.day > base_date.day:
        day = date.day + 1
    else:
        day = date.day
    hour = time.hour
    minute = time.minute
    updated_date = date.replace(day=day, hour=hour, minute=minute)
    return updated_date


def hash_numbers(number):
    """Hash number in words into the corresponding integer value."""
    if re.match(r'one|^a\b', number, re.IGNORECASE):
        return 1
    if re.match(r'two', number, re.IGNORECASE):
        return 2
    if re.match(r'three', number, re.IGNORECASE):
        return 3
    if re.match(r'four', number, re.IGNORECASE):
        return 4
    if re.match(r'five', number, re.IGNORECASE):
        return 5
    if re.match(r'six', number, re.IGNORECASE):
        return 6
    if re.match(r'seven', number, re.IGNORECASE):
        return 7
    if re.match(r'eight', number, re.IGNORECASE):
        return 8
    if re.match(r'nine', number, re.IGNORECASE):
        return 9
    if re.match(r'ten', number, re.IGNORECASE):
        return 10
    if re.match(r'eleven', number, re.IGNORECASE):
        return 11
    if re.match(r'twelve', number, re.IGNORECASE):
        return 12
    if re.match(r'thirteen', number, re.IGNORECASE):
        return 13
    if re.match(r'fourteen', number, re.IGNORECASE):
        return 14
    if re.match(r'fifteen', number, re.IGNORECASE):
        return 15
    if re.match(r'sixteen', number, re.IGNORECASE):
        return 16
    if re.match(r'seventeen', number, re.IGNORECASE):
        return 17
    if re.match(r'eighteen', number, re.IGNORECASE):
        return 18
    if re.match(r'nineteen', number, re.IGNORECASE):
        return 19
    if re.match(r'twenty', number, re.IGNORECASE):
        return 20
    if re.match(r'thirty', number, re.IGNORECASE):
        return 30
    if re.match(r'forty', number, re.IGNORECASE):
        return 40
    if re.match(r'fifty', number, re.IGNORECASE):
        return 50
    if re.match(r'sixty', number, re.IGNORECASE):
        return 60
    if re.match(r'seventy', number, re.IGNORECASE):
        return 70
    if re.match(r'eighty', number, re.IGNORECASE):
        return 80
    if re.match(r'ninety', number, re.IGNORECASE):
        return 90
    if re.match(r'hundred', number, re.IGNORECASE):
        return 100
    if re.match(r'thousand', number, re.IGNORECASE):
        return 1000


# ---- TIME TEXT CLASSES ---- #


class NumberDayRelative:
    """Class for number_day_relative text format."""

    def __init__(self):
        """Initialize class."""
        self.regex = REG1

    def ground_text(self, text, base_date):
        """Ground text that matches regex 1."""
        # split value off from unit and relative phrase
        split_time = re.split(r'\s(?=days?|months?|years?|weeks?)',
                              text.lower())
        value = split_time[0]
        # If numbers are given in words, hash them into corresponding numbers.
        # eg. twenty five days ago --> 25 days ago
        if re.search(NUMBERS, text, re.IGNORECASE):
            num_list = map(lambda s: hash_numbers(s), re.findall(NUMBERS + '+',
                           value, re.IGNORECASE))
            value = sum(num_list)
        # otherwise convert directly to integer for calculation
        else:
            value = int(value)
        # split out unit and relative phrase
        unit = split_time[1]
        split_unit = re.split(r'\s', unit, re.IGNORECASE)
        unit = split_unit[0]
        if(unit[-1] != "s") & (unit[-1] != unicode("s")):
            unit = unit + "s"
        # calculate shift from unit
        kwargs = {unit: value}
        time_shift = relativedelta(**kwargs)
        # apply relative phrase appropriately and shift
        relative_phrase = split_unit[1]
        earlier_phrases = ["before", "earlier", "ago"]
        if relative_phrase in earlier_phrases:
            # we shouldn't have any valid times that are further than 5 years from now.
            if time_shift.years <= 5:
                new_date = base_date - time_shift
                return new_date
        else:
            if time_shift.years <= 5:
                new_date = base_date + time_shift
                return new_date


class RelativeDMY:
    """Class for relative day, month, year text format."""

    def __init__(self):
        """Initialize class."""
        self.regex = REG2

    def ground_text(self, text, base_date):
        """Ground text that matches regex 2."""
        # can split two word phrase on whitespace
        split_time = re.split(r'\s', text)
        relative_phrase = split_time[0]
        unit = split_time[1]
        # deal with unit first
        if re.match(DMY, unit, re.IGNORECASE):
            base_unit = str(unit).lower() + 's'
            time_shift = relativedelta(seconds=0)
        elif re.match(WEEK_DAY, unit, re.IGNORECASE):
            weekday_num = HASH_WEEKDAYS[unit.lower()]
            base_unit = "weeks"
            wkwargs = {'weekday': weekday_num}
            time_shift = relativedelta(**wkwargs)
        elif re.match(MONTH, unit, re.IGNORECASE):
            month_num = HASH_MONTHS[unit.lower()]
            base_unit = "years"
            mkwargs = {'month': month_num}
            time_shift = relativedelta(**mkwargs)
        else:
            time_shift = relativedelta(seconds=0)
        # now adjust using relative phrase
        if relative_phrase == 'this':
            addl_shift = relativedelta(seconds=0)
        elif relative_phrase == 'next':
            nkwargs = {base_unit: 1}
            addl_shift = relativedelta(**nkwargs)
        elif relative_phrase == 'last':
            lkwargs = {base_unit: -1}
            addl_shift = relativedelta(**lkwargs)
        else:
            addl_shift = relativedelta(seconds=0)
        new_date = base_date + time_shift + addl_shift
        return new_date


class RelativeDay:
    """Class for relative day, month, year text format."""

    def __init__(self):
        """Initialize class."""
        self.regex = REG3

    def ground_text(self, text, base_date):
        """Ground text that matches regex 3."""
        if text == 'tomorrow':
            new_date = base_date + relativedelta(days=1)
        elif text == 'yesterday':
            new_date = base_date - relativedelta(days=1)
        else:
            new_date = base_date
        return new_date


class ISO:
    """Class for ISO text format."""

    def __init__(self):
        """Initialize class."""
        self.regex = REG4

    def ground_text(self, text, base_date):
        """Ground text that matches regex 4."""
        dmy = re.split(r'\s', text)[0]  # get rid of any time info
        dmy = re.split(r'/|-', dmy)  # split into fields
        year = int(dmy[0])
        month = int(dmy[1])
        day = int(dmy[2])
        if (1 <= month <= 12):
            if (1 <= day <= 31):
                if (1900 < year < 9999):
                    new_date = datetime(year, month, day)
                    return new_date


class YearOnly:
    """Class for year only format."""

    def __init__(self):
        """Initialize class."""
        self.regex = REG5

    def ground_text(self, text, base_date):
        """Ground text that matches regex 5."""
        year = int(text)
        delta = relativedelta(year=year)
        new_date = base_date + delta
        return new_date


class DayMonth:
    """Class for day/month format."""

    def __init__(self):
        """Initialize class."""
        self.regex = REG6

    def ground_text(self, text, base_date):
        """Ground text that matches regex 6."""
        split_time = re.split(r'[/-]', text)
        # this format is month/day
        month = int(split_time[0])
        day = int(split_time[1])
        if ((month < 13) and (day < 32)):
            delta = relativedelta(month=month, day=day)
        else:
            delta = relativedelta(month=0, day=0)
        # need to handle year boundary, since future date is implied
        if month < base_date.month:
            delta = delta + relativedelta(years=1)
        new_date = base_date + delta
        return new_date


class MonthDay:
    """Class for written month numeric day format."""

    def __init__(self):
        """Initialize class."""
        self.regex = REG7

    def ground_text(self, text, base_date):
        """Ground text that matches regex 7."""
        split_time = re.split(r'\s', text)
        month = HASH_MONTHS[split_time[0].lower()]
        day = int(split_time[1])
        delta = relativedelta(month=month, day=day)
        # need to handle year boundary, since future date is implied
        if month < base_date.month:
            delta = delta + relativedelta(years=1)
        new_date = base_date + delta
        return new_date


class WeekdayOnly:
    """Class for the weekay only format."""

    def __init__(self):
        """Initialize class."""
        self.regex = REG8

    def ground_text(self, text, base_date):
        """Ground text that matches regex 8."""
        split_time = re.split(r'\s', text)
        # handle possible recurrence
        if split_time[0] == 'every':
            day = HASH_WEEKDAYS[split_time[1].lower()]
        else:
            day = HASH_WEEKDAYS[split_time[0].lower()]
        delta = relativedelta(weekday=day)
        new_date = base_date + delta
        return new_date


class Holiday:
    """Class for the holiday format."""

    def __init__(self):
        """Initialize class."""
        self.regex = REG9

    def ground_text(self, text, base_date):
        """Ground text that matches regex 9."""
        # New Years Eve
        if re.match(r'(new year(\')?s( eve)?|nye|#newyearseve)', text, re.IGNORECASE):
            year = base_date.year
            new_date = datetime(year, 12, 31)
        # valentines
        elif re.match(r'valentine(\')?s( day)?', text, re.IGNORECASE):
            year = base_date.year
            new_date = datetime(year, 2, 14)
        # mardi gras
        elif re.match(r'(mardi gras|fat tuesday|shrove tuesday)', text, re.IGNORECASE):
            year = base_date.year
            # easter method returns a date object, need to initialize time for type consistency
            new_date = datetime.combine(easter(year), datetime.min.time()) - relativedelta(days=47)
        # st. patricks
        elif re.match(r'(st patrick(\')?s( day)?|st pattys|st paddys)', text, re.IGNORECASE):
            year = base_date.year
            new_date = datetime(year, 3, 17)
        # easter
        elif re.match(r'easter', text, re.IGNORECASE):
            year = base_date.year
            # easter method returns a date object, need to initialize time for type consistency
            new_date = datetime.combine(easter(year), datetime.min.time())
        # cinco de mayo
        elif re.match(r'cinco de mayo', text, re.IGNORECASE):
            year = base_date.year
            new_date = datetime(year, 5, 5)
        # Mothers day
        elif re.match(r'mother(\')?s day', text, re.IGNORECASE):
            year = base_date.year
            # if 5-1 is a sunday, mothers day will be the next sunday
            if datetime(year, 5, 1).weekday == 6:
                new_date = datetime(year, 5, 1) + relativedelta(weeks=1)
            # otherwise, it will be the second sunday
            else:
                new_date = datetime(year, 5, 1) + relativedelta(weeks=1, weekday=6)
        return new_date


class RecurringDaily:
    """Class for the recurring daily format."""

    def __init__(self):
        """Initialize class."""
        self.regex = REG10

    def ground_text(self, text, base_date):
        """Ground text that matches regex 10."""
        new_date = base_date
        return new_date


class Today:
    """Class for time text referring to today."""

    def __init__(self):
        """Initialize class."""
        self.regex = REG11

    def ground_text(self, text, base_date):
        """Ground text that matches regex 11."""
        new_date = base_date
        return new_date


class TimeAmPm:
    """Class for time text referring to time with am/pm."""

    def __init__(self):
        """Initialize class."""
        self.regex = REG12

    def ground_text(self, text, base_date):
        """Ground text that matches regex 12."""
        # split up tag and grab relevant parts
        time, am_pm = split_am_pm(text)
        # split up numerical portion
        hour, minute = split_hour_minute(time)
        # apply to date as appropriate
        if ((am_pm == "pm") and (hour != 12)):
            hour += 12
        if hour < base_date.hour:
            day = base_date.day + 1
        else:
            day = base_date.day
        new_date = base_date.replace(day=day, hour=hour, minute=minute)
        return new_date


class TimeNoAmPm:
    """Class for time text referring to time without am/pm."""

    def __init__(self):
        """Initialize class."""
        self.regex = REG13

    def ground_text(self, text, base_date):
        """Ground text that matches regex 13."""
        # need to find the subset of the match that contains the numbers.
        # this could be in several locations depending on the match
        split_time = re.findall(r'((\d{1,2})(:\d{1,2})?)', text)
        time = split_time[0][0]  # first match, full match.
        # split up numerical portion
        hour, minute = split_hour_minute(time)
        # as a default, assume hours less than 10 are PM.
        if hour < 10:
            hour += 12
        if hour < base_date.hour:
            day = base_date.day + 1
        else:
            day = base_date.day
        new_date = base_date.replace(day=day, hour=hour, minute=minute)
        return new_date


class TimeRange:
    """Class for time text referring to time ranges."""

    def __init__(self):
        """Initialize class."""
        self.regex = REG14

    def ground_text(self, text, base_date):
        """Ground text that matches regex 14."""
        split_time = re.split(r'-', text)
        parsed_time = []
        for time in split_time:
            time_text, ampm = split_am_pm(time)
            time_dict = {'time': time_text, "ampm": ampm}
            parsed_time.append(time_dict)
        if ((parsed_time[0]['ampm'] is not "") & (parsed_time[1]['ampm'] is not "")):
            for time in parsed_time:
                hour, minute = split_hour_minute(time['time'])
                if ((time['ampm'] == "pm") and (hour != 12)):
                    hour += 12
                time['hour'] = hour
                time['minute'] = minute
        elif ((parsed_time[0]['ampm'] is not "") | (parsed_time[1]['ampm'] is not "")):
            ampm = parsed_time[0]['ampm'] + parsed_time[1]['ampm']
            for time in parsed_time:
                hour, minute = split_hour_minute(time['time'])
                if ((ampm == "pm") and (hour != 12)):
                    hour += 12
                time['hour'] = hour
                time['minute'] = minute
        else:
            for time in parsed_time:
                hour, minute = split_hour_minute(time['time'])
                time['hour'] = hour
                time['minute'] = minute
        for time in parsed_time:
            # generally, times less than 10 will be PMs if not specified
            if time['hour'] < 10:
                time['hour'] += 12
            if time['hour'] < base_date.hour:
                time['day'] = base_date.day + 1
            else:
                time['day'] = base_date.day
            time['new_date'] = base_date.replace(day=time['day'],
                                                 hour=time['hour'],
                                                 minute=time['minute'])
        start_time = parsed_time[0]['new_date']
        end_time = parsed_time[1]['new_date']
        output = [start_time, end_time]
        return output


TIME_RANGE_FORMATS = [TimeRange()]

TIME_FORMATS = [TimeAmPm(), TimeNoAmPm()]

DATE_FORMATS = [NumberDayRelative(), RelativeDMY(), RelativeDay(),
                ISO(), DayMonth(), MonthDay(), WeekdayOnly(), Holiday(),
                YearOnly(), RecurringDaily(), Today()]


# ---- NON -PUBLIC METHODS ---- #


def _tag(text, subbed_text, type):
    """Tag date or time info in text.

    Parameters:
    text: str to tag

    Returns:
    text: tagged text

    """
    # Initialization
    time_found = []
    placeholder = "<SUBBED>"
    if type == "time":
        formats = TIME_FORMATS
        open_tag = '<TIME>'
        close_tag = '</TIME>'
    elif type == 'time_range':
        formats = TIME_RANGE_FORMATS
        open_tag = '<TIME_RANGE>'
        close_tag = '</TIME_RANGE>'
    else:
        formats = DATE_FORMATS
        open_tag = '<DATE>'
        close_tag = '</DATE>'
    # re.findall() finds all the substring matches, keep only the full
    #  matching string. Captures expressions such as 'number of days' ago, etc.
    for time_format in formats:
        for time in time_format.regex.findall(subbed_text):
            # only use the first result if the regex finds a tuple (substring) (reg1 and reg2 esp)
            if len(time) > 1:
                time = time[0]
            time_found.append(time)

    # Tag only temporal expressions which haven't been tagged.
    for time in time_found:
        subbed_text = re.sub(time, placeholder, subbed_text)
        text = re.sub(time + '(?!' + close_tag + ')', open_tag + time + close_tag, text)
    return text, subbed_text


def _ground(text, subbed_text, base_date, type):
    if type == "time":
        formats = TIME_FORMATS
        sub = " <GroundedTime> "
    elif type == "time_range":
        formats = TIME_RANGE_FORMATS
        sub = " <GroundedRange> "
    else:
        formats = DATE_FORMATS
        sub = " <GroundedDate> "
    grounded_times = []
    for time_format in formats:
        # search subbed text to not repeat finds.
        for time in time_format.regex.findall(subbed_text):
            # only use the first result if the regex finds a tuple (substring) (reg1 and reg2 esp)
            if len(time) > 1:
                time = time[0]
            # index MUST come from original text
            index = text.index(time)
            time_grounded = time_format.ground_text(time, base_date)
            time_obj = {"index": index, "type": type, "grouped": False, "date_time": time_grounded}
            grounded_times.append(time_obj)
            subbed_text = re.sub(time, sub, subbed_text)  # sub out for placeholder
    return text, subbed_text, grounded_times


# ---- PUBLIC METHODS ---- #


def tag(text):
    """Tag all temporal expressions in text.

    Parameters:
    text: str to tag

    Returns:
    text: tagged text

    """
    range_tagged, range_subbed = _tag(text, text, "time_range")
    time_tagged, time_subbed = _tag(range_tagged, range_subbed, "time")
    date_tagged, date_subbed = _tag(time_tagged, time_subbed, "date")
    return date_tagged


def ground(text, base_date, replace=False):
    """Time ground text to base date.

    Parameters:
    text: str to ground
    base_date: date object
    replace: bool for replacing time text with a marker

    Returns:
    base_Date Grounded Text

    """
    # initialize
    grounded_times = []
    # do ranges first
    text, cleaned_text, times = _ground(text, text, base_date, "time_range")
    grounded_times.extend(times)
    # do time first
    text, cleaned_text, times = _ground(text, cleaned_text, base_date, "time")
    grounded_times.extend(times)
    # then do date
    text, cleaned_text, times = _ground(text, cleaned_text, base_date, "date")
    grounded_times.extend(times)
    # sort found times by index in string
    sorted_times = sorted(grounded_times, key=lambda k: k['index'])
    char_limit = 45
    # find groups of related and group together into final time list
    final_times = []
    for k, item in enumerate(sorted_times):
        # check that we aren't at the end of
        next_items = [None, None]
        if (k + 1) < len(sorted_times):
            # grab one ahead if possible
            next_items[0] = sorted_times[k + 1]
        if (k + 2) < len(sorted_times):
            # grab two ahead if possible
            next_items[1] = sorted_times[k + 2]
        next_items = filter(None, next_items)
        if item['type'] == 'date':
            if len(next_items) == 0:
                if item['grouped'] is False:
                    final_times.append(item['date_time'])
                    item['grouped'] = True
            else:
                for next_item in next_items:
                    if (((next_item['index'] - item['index']) < char_limit) &
                       (next_item['grouped'] is False)):

                        if next_item['type'] == 'time':
                            new_time = update_date_with_time(item['date_time'],
                                                             next_item['date_time'],
                                                             base_date)
                            final_times.append(new_time)
                            next_item['grouped'] = True
                            item['grouped'] = True
                        elif next_item['type'] == 'time_range':
                            new_start_time = update_date_with_time(item['date_time'],
                                                                   next_item['date_time'][0],
                                                                   base_date)
                            new_end_time = update_date_with_time(item['date_time'],
                                                                 next_item['date_time'][1],
                                                                 base_date)
                            final_times.append(new_start_time)
                            final_times.append(new_end_time)
                            next_item['grouped'] = True
                            item['grouped'] = True
                        else:
                            # if at any point we hit a non-time in next next_items
                            # subsequent nexts cannot be associated, we should exit loop.
                            break
                if item['grouped'] is False:
                    final_times.append(item['date_time'])
                    item['grouped'] = True
        elif item['type'] == 'time_range':
            if item['grouped'] is False:
                for time in item['date_time']:
                    final_times.append(time)
                    item['grouped'] = True
        else:
            if item['grouped'] is False:
                final_times.append(item['date_time'])
                item['grouped'] = True
    # output results
    if replace is True:
        return cleaned_text, final_times
    else:
        return final_times
