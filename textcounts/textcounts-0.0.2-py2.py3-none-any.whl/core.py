import pandas as pd

def conditional_lower(input_string, tolower_bool):
    """
    Converts string to lowercase based on a conditional value. Helper function
    used to make search_series more readable.
    """
    if tolower_bool:
        return input_string.lower()
    else:
        return input_string
    
def search_series(series, patterns, exclude=None, ignore_case=True):
    """
    Searches a series for patterns, returning matching items and frequency counts. This
    is more of a helper function than intended to be called directly, but it can be.
    
    Parameters:
        series: an iterable object, such as a list
        patterns: a single string or a list of strings to match
        exclude: a single string or a list of strings to remove before counting
    
    Returns:
        tuple of (pattern_match, freq_counts)
        pattern_match: list of strings matching at least one of the patterns
        freq_counts: dict of {series item number : count of any patterns in series item}
    
    """
    
    series_len = len(series)
    pattern_match = []
    freq_counts = {}
    series_count = 0
    if type(patterns) is not list:
        patterns = [patterns]
    
    for item in series:
        match_count = 0
        if exclude is not None:
            if type(exclude) is list:
                for i in exclude:
                    item_parse = conditional_lower(item, ignore_case).replace(exclude, "")
            else:
                item_parse = item.lower().replace(exclude, "")
        else:
            item_parse = item.lower()
            
        
        for pattern in patterns:
        
            if item_parse.find(pattern) >= 0:
                match_count = match_count + item_parse.count(pattern)
                if len(pattern_match) == 0 or pattern_match[-1] != item:
                    pattern_match.append(item)
                
        freq_counts[series_count] = match_count
        series_count = series_count + 1
    return pattern_match, freq_counts

def find_mentions(series, patterns, exclude=None, ignore_case=True):
    """
    Searches a series for patterns, returning matching items. A wrapper around
    search_series().
    
    Parameters:
        series: an iterable object, such as a list
        patterns: a single string or a list of strings to match
        exclude: a single string or a list of strings to remove before counting
    
    Returns:
        tuple of (pattern_match, freq_counts)
        pattern_match: list of strings matching at least one of the patterns
        freq_counts: dict of {series item number : count of any patterns in series item}
    """
    
    
    return search_series(series, patterns, exclude, ignore_case)[0]
    
def prop_mentions(series, patterns, exclude=None, ignore_case=True):
    """
    Return the proportion of items in series that match at least one pattern.
    """
    pattern_match = search_series(series, patterns, exclude, ignore_case=True)[0]
    return len(pattern_match)/len(series)


def pattern_counts(series, patterns_iter, exclude=None, ignore_case=True):
    """
    Search series for a set of patterns, returning a dataframe of frequency counts
    
    Parameters:
        series: an iterable object to search through, such as a list
        patterns_iter: a list of dict of patterns:
            if list: a list of strings, counts will be made for each string
            if dict: a dict of pattern labels (strings) and patterns (strings or lists of strings)
        exclude: a single string or a list of strings to remove before counting
        
    Returns:
        counts_df: a pandas dataframe. Rows are each item in series, columns are
                   each item in pattern_iter. Value is the number of times any 
                   pattern appears in each item.
    """
    if type(patterns_iter) == dict:
        patterns_dict = patterns_iter
    elif type(patterns_iter) == list:
        patterns_dict = {}
        for item in patterns_iter:
            patterns_dict[item] = item
    elif type(patterns_iter) == str:
        patterns_dict = {patterns_iter:patterns_iter}
    else:
        raise Exception("patterns_iter must be a dict, list, or string")
    
    df_counts_dict = {}
    
    for patterns_name, patterns in patterns_dict.items():
        df_counts_dict[patterns_name] = pd.DataFrame.from_dict(search_series(series, patterns, exclude, ignore_case)[1], orient="index")
        df_counts_dict[patterns_name].index.name = 'location'
        df_counts_dict[patterns_name].columns = [patterns_name + ' count']
        
    return pd.concat(df_counts_dict.values(), axis=1)

def pattern_prop(series, patterns_iter, exclude=None, ignore_case=True):
    """
    Search series for a set of patterns, returning a dataframe used for counting proportions.
    
    Parameters:
        series: an iterable object to search through, such as a list
        patterns_iter: a list of dict of patterns:
            if list: a list of strings, counts will be made for each string
            if dict: a dict of pattern labels (strings) and patterns (strings or lists of strings)
        exclude: a single string or a list of strings to remove before counting
        
    Returns:
        counts_df: a pandas dataframe. Rows are each item in series, columns are
                   each item in pattern_iter. Value is 1 if any pattern appears
                   in each item, 0 if not.
    """    
    if type(patterns_iter) == dict:
        patterns_dict = patterns_iter
    elif type(patterns_iter) == list:
        patterns_dict = {}
        for item in patterns_iter:
            patterns_dict[item] = item
    elif type(patterns_iter) == str:
        patterns_dict = {patterns_iter:patterns_iter}
    else:
        raise Exception("patterns_iter must be a dict, list, or string")
    
    df_counts_dict = {}
    
    for patterns_name, patterns in patterns_dict.items():
        df_counts_dict[patterns_name] = pd.DataFrame.from_dict(search_series(series, patterns, exclude, ignore_case)[1], orient="index")
        df_counts_dict[patterns_name].index.name = 'location'
        df_counts_dict[patterns_name].columns = [patterns_name]
        
    return pd.concat(df_counts_dict.values(), axis=1).astype(bool).astype(int)