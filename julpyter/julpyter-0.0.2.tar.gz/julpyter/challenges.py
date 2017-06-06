# functions for converting notebooks to learn-style markdown challenges

import pandas as pd
from tabulate import tabulate
from .challenge import *

def make_coding(nb, uuid):
    """Make a learn coding challenge from a jupyter notebook

    Parameters
    ----------
    nb : a jupyter notebook json string
    uuid : unique universal identifier for the challenge

    """
    title = get_source(nb['cells'], 'title')
    title = title.strip('#').strip()

    question = get_source(nb['cells'], tag='question')
    question = to_mathjax(question)

    placeholder = get_source(nb['cells'], tag='placeholder')
    placeholder = strip_magic(placeholder)
    placeholder = strip_solution(placeholder)

    tests = get_source(nb['cells'], tag='tests')
    tests = strip_magic(tests)

    explanation = get_source(nb['cells'], tag='explanation')
    explanation = to_mathjax(explanation)
    solution = get_solution(tests)
    lines = explanation.split('\n')
    lines.append('')
    lines.extend(solution)
    explanation = '\n'.join(lines)

    challenge = \
f"""### !challenge

* type: code-snippet
* language: python3.6
* id: {uuid}
* title: {title}

### !question
{question}
### !end-question

### !placeholder

```python
{placeholder}
```
### !end-placeholder

### !tests
```python
{tests}
```
### !end-tests

### !explanation
{explanation}
### !end-explanation

### !end-challenge"""

    video = get_source(nb['cells'], tag='video')
    if not video:
        return challenge

    lines = challenge.split('\n')
    lines.append('## Worked Solution')
    lines.append('')
    lines.append(video)
    challenge = '\n'.join(lines)
    return challenge

def make_multiple_choice(nb, uuid):
    """Make a learn multiple challenge from a jupyte notebook

    Parameters
    ----------
    nb : a jupyter notebook json string
    uuid : unique universal identifier for the challenge

    """
    title = get_source(nb['cells'], 'title')
    title = title.strip('#').strip()

    question = get_source(nb['cells'], tag='question')
    question = to_mathjax(question)

    options = get_source(nb['cells'], tag='options')
    options = to_mathjax(options)

    answer = get_source(nb['cells'], tag='answer')
    answer = to_mathjax(answer)

    explanation = get_source(nb['cells'], tag='explanation')
    explanation = to_mathjax(explanation)

    return \
f"""### !challenge

* type: multiple-choice
* id: {uuid}
* title: {title}

### !question
{question}
### !end-question

### !options
{options}
### !end-options

### !answer
{answer}
### !end-answer

### !explanation
{explanation}
### !end-explanation

### !end-challenge"""

def make_paragraph(nb, uuid):
    """Make a paragraph challenge from a jupyter notebook

    Parameters
    ----------
    nb : a jupyter notebook json string
    uuid : unique universal identifier for the challenge

    """

    title = get_source(nb['cells'], 'title')
    title = title.strip('#').strip()

    question = get_source(nb['cells'], tag='question')
    question = to_mathjax(question)

    placeholder = get_source(nb['cells'], tag='placeholder')
    placeholder = to_mathjax(placeholder)

    explanation = get_source(nb['cells'], tag='explanation')
    explanation = to_mathjax(explanation)

    return \
f"""### !challenge

* type: paragraph
* id: {uuid}
* title: {title}

### !question
{question}
### !end-question

### !placeholder
{placeholder}
### !end-placeholder

### !explanation
{explanation}
### !end-explanation

### !end-challenge"""

def make_number(nb, uuid, decimal=5):
    """Make a number challenge from a jupyter notebook

    Parameters
    ----------
    nb : a jupyter notebook json string
    uuid : unique universal identifier for the challenge

    """

    title = get_source(nb['cells'], 'title')
    title = title.strip('#').strip()

    question = get_source(nb['cells'], tag='question')
    question = to_mathjax(question)

    placeholder = get_source(nb['cells'], tag='placeholder')
    placeholder = to_mathjax(placeholder)

    answer = get_source(nb['cells'], tag='answer')
    answer = to_mathjax(answer)

    explanation = get_source(nb['cells'], tag='explanation')
    explanation = to_mathjax(explanation)

    return \
f"""### !challenge

* type: number
* id: {uuid}
* title: {title}
* decimal: {decimal}

### !question
{question}
### !end-question

### !placeholder
{placeholder}
### !end-placeholder

### !answer
{answer}
### !end-answer

### !explanation
{explanation}
### !end-explanation

### !end-challenge"""

def make_raw(nb, uuid):
    """Convert notebook to markdown

    Parameters
    ----------
    nb : a jupyter notebook json string

    Format code nice.

    """
    lines = []
    for cell in nb['cells']:
        if cell['cell_type'] == 'markdown':
            lines += cell['source']
        elif cell['cell_type'] == 'code':
            lines += ['```python']
            lines += cell['source']
            lines += ['```']

    markdown = ''.join(lines)
    markdown = to_mathjax(markdown)
    return markdown
