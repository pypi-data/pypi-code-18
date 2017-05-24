import collections
import re
import shlex
import string

import dockerfile_parse
import six


def create_dockerfile_structure(dockerfile_content):
    dfp = dockerfile_parse.DockerfileParser(fileobj=dockerfile_content,
                                            cache_content=True,
                                            env_replace=False)

    commands = dfp.structure
    env_label_context = dfp.context_structure
    base_image = dfp.baseimage
    return commands, env_label_context, base_image


def apply_shell_expansion(str):
    """
    Use shlex to expand string. (like echo)
        e.g. "string with "space -> string with space
    :param str: string to apply an expansion
    :return: shell-expanded string
    """
    return " ".join(shlex.split(str))


_find_unsafe = re.compile(r'[^\w@%+=:,./-]').search


def _quote_from_shlex(s):
    """
    Return a shell-escaped version of the string *s*.
    (implementation from shlex for python3)
    """
    if not s:
        return "''"
    if _find_unsafe(s) is None:
        return s

    # use single quotes, and put single quotes into double quotes
    # the string $'b is then quoted as '$'"'"'b'
    return "'" + s.replace("'", "'\"'\"'") + "'"


def quote(s):
    """
    Quote the string to be agnostic to shell expansion.
    (Use implementation from shlex.)

    :param s: string to quote
    :return: shell-quoted string
    """
    if six.PY3:
        return shlex.quote(s)
    else:
        return _quote_from_shlex(s)


def substitute_variables(s, variables):
    """
    Make a variable substitution.

    :param s: text to apply substitution on
    :param variables: (dict) environment variables
    :return: string s with substituted variables
    """

    s = s.replace("\\$", "$$")

    regex = "{([^}]*:-[^}]*)}"
    matches = re.finditer(regex, s)
    for m in matches:
        key, val = m.group(1).split(":-")
        variables.setdefault(key, val)

    regex_subst = "\$({[^}]*):-[^}]*}"
    s = re.sub(regex_subst, "$\g<1>}", s, 0)

    d = collections.defaultdict(lambda: "")
    d.update(variables)
    t = string.Template(s)
    substituted = t.substitute(d)
    return substituted


def get_name_and_tag(name):
    name_parts = name.split(':')
    if len(name_parts) == 2:
        repo = name_parts[0]
        tag = name_parts[1]
    else:
        repo = name
        tag = "latest"

    return repo, tag
