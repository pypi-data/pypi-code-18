import re

def repl(m):
    # Convert hex to int to unicode character
    chr_code = int(m.group(1), 16)
    return unichr(chr_code)

def entity_to_unicode(s):
    """
    Quick convert unicode HTML entities to unicode characters
    using a regular expression replacement
    """
    # Selected character replacements that have been seen
    replacements = []
    replacements.append((r"&alpha;", u"\u03b1"))
    replacements.append((r"&beta;", u"\u03b2"))
    replacements.append((r"&gamma;", u"\u03b3"))
    replacements.append((r"&delta;", u"\u03b4"))
    replacements.append((r"&epsilon;", u"\u03b5"))
    replacements.append((r"&ordm;", u"\u00ba"))
    replacements.append((r"&iuml;", u"\u00cf"))
    replacements.append((r"&ldquo;", '"'))
    replacements.append((r"&rdquo;", '"'))

    # First, replace numeric entities with unicode
    s = re.sub(r"&#x(....);", repl, s)
    # Second, replace some specific entities specified in the list
    for entity, replacement in replacements:
        s = re.sub(entity, replacement, s)
    return s

def xml_escape_ampersand(s):
    """
    Quick convert unicode ampersand characters not associated with
    a numbered entity or not starting with allowed characters to a plain &amp;
    """
    start_with_match = "(\#x(....);|lt;|gt;|amp;)"
    # The pattern below is match & that is not immediately followed by #
    s = re.sub(r"&(?!" + start_with_match + ")", '&amp;', s)
    return s

def replace_tags(s, from_tag='i', to_tag='italic'):
    """
    Replace tags such as <i> to <italic>
    <sup> and <sub> are allowed and do not need to be replaced
    This does not validate markup
    """
    s = s.replace('<' + from_tag + '>', '<' + to_tag + '>')
    s = s.replace('</' + from_tag + '>', '</' + to_tag + '>')
    return s

def escape_unmatched_angle_brackets(s):
    """
    In order to make an XML string less malformed, escape
    unmatched less than tags that are not part of an allowed tag
    Note: Very, very basic, and do not try regex \1 style replacements
      on unicode ever again! Instead this uses string replace
    """
    allowed_tags = ['<i>', '</i>',
                    '<italic>', '</italic>',
                    '<b>', '</b>',
                    '<bold>', '</bold>',
                    '<sup>', '</sup>',
                    '<sub>', '</sub>',
                    '<u>', '</u>',
                    '<underline>', '</underline>',
                    '<b>', '</b>',
                    '<bold>', '</bold>',
                    '<p>', '</p>']

    # Split string on tags
    tags = re.split('(<.*?>)', s)
    #print tags

    for i in range(len(tags)):
        val = tags[i]

        # Use angle bracket character counts to find unmatched tags
        #  as well as our allowed_tags list to ignore good tags

        if val.count('<') == val.count('>') and val not in allowed_tags:
            val = val.replace('<', '&lt;')
            val = val.replace('>', '&gt;')
        else:
            # Count how many unmatched tags we have
            while val.count('<') != val.count('>'):
                if val.count('<') != val.count('>') and val.count('<') > 0:
                    val = val.replace('<', '&lt;', 1)
                elif val.count('<') != val.count('>') and val.count('>') > 0:
                    val = val.replace('>', '&gt;', 1)
            if val.count('<') == val.count('>') and val not in allowed_tags:
                # Send it through again in case there are nested unmatched tags
                val = escape_unmatched_angle_brackets(val)

        tags[i] = val

    return ''.join(tags)
