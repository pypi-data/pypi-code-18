# helper functions for processing learn challenges written in notebooks

import numpy as np
import pandas as pd

def get_solution(tests):
    """Parse out the solution from a coding challenge test class

    Parameters
    ----------
    test : a code cell containing a test class

    There must be a `solution()` method

    """
    lines = tests.split('\n')
    i = 0
    while True:
        line = lines[i]
        if not 'def solution' in line:
            i += 1
            continue
        else:
            break
            
    i += 1
    solution = []
    while True:
        line = lines[i]
        if not line.strip():
            break

        solution.append(line)
        i += 1

    solution = ['```python'] + solution[:-1] + ['```']
    return solution

def strip_magic(s):
    """Strip magic and comments from the beginning of a code cell

    Parameters
    ----------
    s : a code cell beginning with magic and/or comments

    """
    lines = s.split('\n')
    i = 0
    while True:
        line = lines[i]
        if not line or line.startswith('%%') or line.startswith('#'):
            i += 1
            continue
        else:
            break

    lines = lines[i:]
    s = '\n'.join(lines)
    return s

def strip_solution(s):
    """Remove the solution from a code cell

    Parameters
    ----------
    s : a code cell

    This is currently not used anywhere.

    """
    lines = s.split('\n')
    xformed_lines = []
    OUT, IN = True, False
    for line in lines:
        if OUT:
            if line.strip() == '### BEGIN SOLUTION':
                IN, OUT = True, False
            else:
                xformed_lines.append(line)
        else:
            assert IN
            if line.strip() == '### END SOLUTION':
                OUT, IN = True, False
                line = line.replace('### END SOLUTION', 'pass')
                xformed_lines.append(line)
            else:
                continue

    s = '\n'.join(xformed_lines)
    return s

def to_mathjax(text):
    """Convert jupyter-style LaTeX to learn-style MathJax

    Parameters
    ----------
    text : a code cell containing jupyter-style LaTeX

    The only substitutions that are made are
    - \\ -> \\\
    - $...$ -> \\(...\\)

    It's assumed that $$ do not appear inline (i.e. the only place they appear
    is on their own line.

    """
    lines = text.split('\n')
    lines = [line.replace(r'\\', '\\\\\\') for line in lines]
    lines = [line.replace(r'\{', '\\\\{') for line in lines]
    lines = [line.replace(r'\}', '\\\\}') for line in lines]

    xformed_lines = []
    for line in lines:
        if line == '$$':
            xformed_lines.append(line)
            continue

        OUT, IN = True, False
        xformed_line = []
        for c in line:
            if not c == '$':
                xformed_line.append(c)
                continue

            if OUT:
                IN, OUT = True, False
                xformed_line.append(r'\\(')
            elif IN:
                OUT, IN = True, False
                xformed_line.append(r'\\)')

        xformed_line = ''.join(xformed_line)
        xformed_lines.append(xformed_line)

    xformed_text = '\n'.join(xformed_lines)
    return xformed_text

def get_source(cells, tag):
    """Get the contents of a code cell by tag

    Parameters
    ----------
    cells : list of jupyter notebook cells
    tag : tag name

    """
    for cell in cells:
        metadata = cell['metadata']
        if 'tags' not in metadata:
            continue # no tags
        
        if tag in metadata['tags']:
            lines = cell['source'] 
            source = ''.join(lines)
            return source
