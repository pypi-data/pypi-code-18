#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

'''
TGrep search implementation for CONLL-U data (depgrep).

Original copyright:

(c) 16 March, 2013 Will Roberts <wildwilhelm@gmail.com>.

Modified January 2016 for Dependencies in CONLL-U format by Daniel McDonald.
The remainder of this file does not flag changes made to the original.

This module supports TGrep2-style syntax for matching CONLL-U data, stored
in pandas objects.

Tgrep tutorial:
http://www.stanford.edu/dept/linguistics/corpora/cas-tut-tgrep.html
Tgrep2 manual:
http://tedlab.mit.edu/~dr/Tgrep2/tgrep2.pdf
Tgrep2 source:
http://tedlab.mit.edu/~dr/Tgrep2/

The major changes, needed for dependency grammars:

- Parent and child are replaced by governor and dependent, respectively.
- Ability to match not only word forms, but lemma, function, POS, NER, etc. To
  do this, a single alphabetical character is placed before the boundaries of
  a string of regular expression. So, /NN.*/ might become p/NN.*/. Therefore,
  to match dependency graphs with a root node whose lemma is diagnose, and which
  has a dependent, prominal, passivised subject "I", we could write:

  f"root" & l"diagnose" < (p/PRP/ & f"nsubjpass" & w"I")

If this flag is left off, the word form will be searched.

This implementation is (somewhat awkwardly) based on lambda functions
which are predicates on a node.  A predicate is a function which is
either True or False; using a predicate function, we can identify sets
of nodes with particular properties.  A predicate function, could, for
instance, return True only if a particular node has a label matching a
particular regular expression, and has a daughter node which has no
sisters.  Because tgrep2 search strings can do things statefully (such
as substituting in macros, and binding nodes with node labels), the
actual predicate function is declared with three arguments::

    pred = lambda n, m, l: return True # some logic here

`n` is a node in a tree; this argument must always be given
`m` contains a dictionary, mapping macro names onto predicate functions
`l` is a dictionary to map node labels onto nodes in the tree

`m` and `l` are declared to default to `None`, and so need not be
specified in a call to a predicate.  Predicates which call other
predicates must always pass the value of these arguments on.  The
top-level predicate (constructed by `_tgrep_exprs_action`) binds the
macro definitions to `m` and initialises `l` to an empty dictionary.
'''

from __future__ import print_function, unicode_literals
try:
    from builtins import bytes, range, str
except ImportError:
    print('Warning: depgrep may not work correctly on Python 2.* without the')
    print('`future` package installed.')
import functools
try:
    import pyparsing
except ImportError:
    print('Warning: depgrep will not work without the `pyparsing` package')
    print('installed.')
import re

class TgrepException(Exception):
    '''Tgrep exception type.'''
    pass

def ancestors(node, df):
    '''
    Returns the list of all nodes dominating the given tree node.
    This method will not work with leaf nodes, since there is no way
    to recover the parent.
    '''
    ancestors = []
    gov = node['g']
    sent = df.xs[node.name[0], node.name[1]]
    while gov:
        gov_tok = sent.loc[gov]
        ancestors.append(gov_tok)
        gov = gov_tok['g']
    return ancestors

def unique_ancestors(node, sent):
    '''
    Returns the list of all nodes dominating the given node, where
    there is only a single path of descent.
    '''
    raise NotImplementedError
    results = []
    try:
        current = node.parent()
    except AttributeError:
        # if node is a leaf, we cannot retrieve its parent
        return results
    while current and len(current) == 1:
        results.append(current)
        current = current.parent()
    return results

def _descendants(node, df, recurse=0):
    '''
    Returns the list of all nodes which are descended from the given
    tree node in some way.
    '''
    descendants = []
    # may or may not have to cut down the df
    if len(df.index.names) == 1:
        sent = df 
    else:
        sent = df.xs[node.name[0], node.name[1]]
    desc_str = node['d']
    if desc_str in ['_', 0, '0'] or recurse > 4:
        return []
    descs = [int(i) for i in desc_str.split(',')]
    for d in descs:
        d_tok = sent.loc[d]
        subdesc = _descendants(d_tok, sent, recurse=recurse+1)
        for i in subdesc:
            descendants.append(i)
    return descendants

def _leftmost_descendants(node, sent):
    '''
    Returns the set of all nodes descended in some way through
    left branches from this node.
    '''
    raise NotImplementedError
    try:
        treepos = node.treepositions()
    except AttributeError:
        return []
    return [node[x] for x in treepos[1:] if all(y == 0 for y in x)]

def _rightmost_descendants(node, sent):
    '''
    Returns the set of all nodes descended in some way through
    right branches from this node.
    '''
    raise NotImplementedError
    try:
        rightmost_leaf = max(node.treepositions())
    except AttributeError:
        return []
    return [node[rightmost_leaf[:i]] for i in range(1, len(rightmost_leaf) + 1)]

def _unique_descendants(node, sent):
    '''
    Returns the list of all nodes descended from the given node, where
    there is only a single path of descent.
    '''
    raise NotImplementedError
    results = []
    current = node
    while current and has_dependent(current) and len(current) == 1:
        current = current[0]
        results.append(current)
    return results

def _before(node, df):
    '''
    Returns the set of all nodes that are before the given node.
    '''
    f, s, i = node.name
    matches = df.loc[f,s,slice(None, i-1)]
    return [matches.loc[i] for i in matches.index]

def _immediately_before(node, df):
    '''
    Returns the set of all nodes that are immediately before the given
    node.

    Tree node A immediately precedes node B if the last terminal
    symbol (word) produced by A immediately precedes the first
    terminal symbol produced by B.
    '''
    f, s, i = node.name
    try:
        return [df.loc[f, s, i-1]]
    except:
        return []

def _after(node, df):
    '''
    Returns the set of all nodes that are after the given node.
    '''
    f, s, i = node.name
    matches = df.loc[f,s,slice(i+1, None)]
    return [matches.loc[i] for i in matches.index]

def _immediately_after(node, df):
    '''
    Returns the set of all nodes that are immediately after the given
    node.

    Tree node A immediately follows node B if the first terminal
    symbol (word) produced by A immediately follows the last
    terminal symbol produced by B.
    '''
    f, s, i = node.name
    try:
        return [df.loc[f, s, i+1]]
    except:
        return []

def row_attr(node, attr=False, cs=False):
    '''
    Gets the string value of a given parse tree node, for comparison
    using the tgrep node literal predicates.
    '''
    import pandas as pd
    if isinstance(node, pd.Series):
        nd = node[attr]
    else:
        nd = str(node)
    if cs:
        return nd
    else:
        return nd.lower()

def _tgrep_macro_use_action(_s, _l, tokens):
    '''
    Builds a lambda function which looks up the macro name used.
    '''
    assert len(tokens) == 1
    assert tokens[0][0] == '@'
    macro_name = tokens[0][1:]
    def macro_use(n, m=None, l=None):
        if m is None or macro_name not in m:
            raise TgrepException('macro {0} not defined'.format(macro_name))
        return m[macro_name](n, m, l)
    return macro_use

def _tgrep_node_action(_s, _l, tokens, case_sensitive=False):
    '''
    Builds a lambda function representing a predicate on a tree node
    depending on the name of its node.
    '''
    # print 'node tokens: ', tokens
    if tokens[0] == "'":
        # strip initial apostrophe (tgrep2 print command)
        tokens = tokens[1:]
    if len(tokens) > 1:
        # disjunctive definition of a node name
        assert list(set(tokens[1::2])) == ['|']
        # recursively call self to interpret each node name definition
        tokens = [_tgrep_node_action(None, None, [node])
                  for node in tokens[::2]]
        # capture tokens and return the disjunction
        return (lambda t: lambda n, m=None, l=None: any(f(n, m, l) for f in t))(tokens)
    else:
        if hasattr(tokens[0], '__call__'):
            # this is a previously interpreted parenthetical node
            # definition (lambda function)
            return tokens[0]

        if tokens[0][0] in ['w', 'l', 'p', 'i', 'f', 'e'] \
            and not tokens[0].startswith('i@'):
            attr = tokens[0][0]
            tokens[0] = tokens[0][1:]
        else:
            attr = 'w'

        if tokens[0] == '*' or tokens[0] == '__':
            return lambda n, m=None, l=None: True
        elif tokens[0].startswith('"'):
            assert tokens[0].endswith('"')
            node_lit = tokens[0][1:-1].replace('\\"', '"').replace('\\\\', '\\')
            if not case_sensitive:
                node_lit = node_lit.lower()
            return (lambda s: lambda n, m=None, l=None: row_attr(n, attr,
                    cs=case_sensitive) == s)(node_lit)
        elif tokens[0].startswith('/'):
            assert tokens[0].endswith('/')
            node_lit = tokens[0][1:-1]
            if not case_sensitive:
                node_lit = '(?i)' + node_lit
            return (lambda r: lambda n, m=None, l=None:
                    r.search(row_attr(n, attr, cs=case_sensitive)))(re.compile(node_lit))
        elif tokens[0].startswith('i@'):
            node_func = _tgrep_node_action(_s, _l, [tokens[0][2:].lower()])
            return (lambda f: lambda n, m=None, l=None:
                    f(row_attr(n, attr, cs=case_sensitive).lower()))(node_func)
        else:
            return (lambda s: lambda n, m=None, l=None:
                    row_attr(n, attr, cs=case_sensitive) == s)(tokens[0])

def _tgrep_parens_action(_s, _l, tokens):
    '''
    Builds a lambda function representing a predicate on a tree node
    from a parenthetical notation.
    '''
    # print 'parenthetical tokens: ', tokens
    assert len(tokens) == 3
    assert tokens[0] == '('
    assert tokens[2] == ')'
    return tokens[1]

def _tgrep_nltk_tree_pos_action(_s, _l, tokens):
    '''
    Builds a lambda function representing a predicate on a tree node
    which returns true if the node is located at a specific tree
    position.
    '''
    # recover the tuple from the parsed sting
    node_tree_position = tuple(int(x) for x in tokens if x.isdigit())
    # capture the node's tree position
    return (lambda i: lambda n, m=None, l=None: (hasattr(n, 'treeposition') and
                                                 n.treeposition() == i))(node_tree_position)

def _tgrep_relation_action(_s, _l, tokens, df):
    '''
    Builds a lambda function repredfing a predicate on a tree node
    depending on its relation to other nodes in the tree.
    '''
    # print 'relation tokens: ', tokens
    # process negation first if needed

    from corpkit.conll import dependents, has_dependent, has_governor, governors, sisters
    #print(df.head(5))

    negated = False
    if tokens[0] == '!':
        negated = True
        tokens = tokens[1:]
    if tokens[0] == '[':
        # process square-bracketed relation expressions
        assert len(tokens) == 3
        assert tokens[2] == ']'
        retval = tokens[1]
    else:
        # process operator-node relation expressions
        assert len(tokens) == 2
        operator, predicate = tokens
        # A = B      A and B are the same node
        if operator == '=' or operator == '&':
            retval = lambda n, m=None, l=None: (predicate(n, m, l))
        # A < B       A is the parent of (immediately dominates) B.
        elif operator == '<':
            retval = lambda n, m=None, l=None: (has_dependent(n) and
                                                any(predicate(x, m, l) for x in dependents(n, df)))
        # A > B       A is the child of B.
        elif operator == '>':
            retval = lambda n, m=None, l=None: (has_governor(n) and
                                                predicate(governors(n, df)[0], m, l))
        # A <, B      Synonymous with A <1 B.
        elif operator == '<,' or operator == '<1':
            retval = lambda n, m=None, l=None: (has_dependent(n) and
                                                predicate(n[0], m, l))
        # A >, B      Synonymous with A >1 B.
        elif operator == '>,' or operator == '>1':
            retval = lambda n, m=None, l=None: (
                                                has_governor(n) and
                                                (n is governors(n, df)[0]) and
                                                predicate(governors(n, df), m, l))
        # A <N B      B is the Nth child of A (the first child is <1).
        elif operator[0] == '<' and operator[1:].isdigit():
            idx = int(operator[1:])
            # capture the index parameter
            retval = (lambda i: lambda n, m=None, l=None: (has_dependent(n) and
                                                           0 <= i < len(dependents(n, df)) and
                                                           predicate(n[i], m, l)))(idx - 1)
        # A >N B      A is the Nth child of B (the first child is >1).
        elif operator[0] == '>' and operator[1:].isdigit():
            idx = int(operator[1:])
            # capture the index parameter
            retval = (lambda i: lambda n, m=None, l=None: (
                                                           has_governor(n) and
                                                           0 <= i < len(governors(n, df)) and
                                                           (n is governors(n, df)[i]) and
                                                           predicate(governors(n, df), m, l)))(idx - 1)
        # A <' B      B is the last child of A (also synonymous with A <-1 B).
        # A <- B      B is the last child of A (synonymous with A <-1 B).
        elif operator == '<\'' or operator == '<-' or operator == '<-1':
            retval = lambda n, m=None, l=None: (has_dependent(n)
                                                and predicate(n[-1], m, l))
        # A >' B      A is the last child of B (also synonymous with A >-1 B).
        # A >- B      A is the last child of B (synonymous with A >-1 B).
        elif operator == '>\'' or operator == '>-' or operator == '>-1':
            retval = lambda n, m=None, l=None: (
                                                has_governor(n) and
                                                (n is governors(n, df)[-1]) and
                                                predicate(governors(n, df), m, l))
        # A <-N B     B is the N th-to-last child of A (the last child is <-1).
        elif operator[:2] == '<-' and operator[2:].isdigit():
            idx = -int(operator[2:])
            # capture the index parameter
            retval = (lambda i: lambda n, m=None, l=None: (has_dependent(n) and
                                                           0 <= (i + len(dependents(n, df))) < len(dependents(n, df)) and
                                                           predicate(n[i + len(dependents(n, df))], m, l)))(idx)
        # A >-N B     A is the N th-to-last child of B (the last child is >-1).
        elif operator[:2] == '>-' and operator[2:].isdigit():
            idx = -int(operator[2:])
            # capture the index parameter
            retval = (lambda i: lambda n, m=None, l=None:
                          (
                           has_governor(n) and
                           0 <= (i + len(governors(n, df))) < len(governors(n, df)) and
                           (n is governors(n, df)[i + len(governors(n, df))]) and
                           predicate(governors(n, df), m, l)))(idx)
        # A <: B      B is the only child of A
        elif operator == '<:':
            retval = lambda n, m=None, l=None: (has_dependent(n) and
                                                len(dependents(n, df)) == 1 and
                                                predicate(n[0], m, l))

        # A >: B      A is the only child of B.
        elif operator == '>:':
            retval = lambda n, m=None, l=None: (
                                                has_governor(n) and
                                                len(governors(n, df)) == 1 and
                                                predicate(governors(n, df), m, l))
        # A << B      A dominates B (A is an ancestor of B).
        elif operator == '<<':
            retval = lambda n, m=None, l=None: (has_dependent(n) and
                                                any(predicate(x, m, l) for x in _descendants(n, df)))
        # A >> B      A is dominated by B (A is a descendant of B).
        elif operator == '>>':
            retval = lambda n, m=None, l=None: any(predicate(x, m, l) for x in ancestors(n, df))
        # A <<, B     B is a left-most descendant of A.
        elif operator == '<<,' or operator == '<<1':
            retval = lambda n, m=None, l=None: (has_dependent(n) and
                                                any(predicate(x, m, l)
                                                    for x in _leftmost_descendants(n, df)))
        # A >>, B     A is a left-most descendant of B.
        elif operator == '>>,':
            retval = lambda n, m=None, l=None: any((predicate(x, m, l) and
                                                    n in _leftmost_descendants(x))
                                                   for x in ancestors(n, df))
        # A <<' B     B is a right-most descendant of A.
        elif operator == '<<\'':
            retval = lambda n, m=None, l=None: (has_dependent(n) and
                                                any(predicate(x, m, l)
                                                    for x in _rightmost_descendants(n, df)))
        # A >>' B     A is a right-most descendant of B.
        elif operator == '>>\'':
            retval = lambda n, m=None, l=None: any((predicate(x, m, l) and
                                                    n in _rightmost_descendants(x))
                                                   for x in ancestors(n, df))
        # A <<: B     There is a single path of descent from A and B is on it.
        elif operator == '<<:':
            retval = lambda n, m=None, l=None: (has_dependent(n) and
                                                any(predicate(x, m, l)
                                                    for x in _unique_descendants(n, df)))
        # A >>: B     There is a single path of descent from B and A is on it.
        elif operator == '>>:':
            retval = lambda n, m=None, l=None: any(predicate(x, m, l) for x in unique_ancestors(n, df))
        # A . B       A immediately precedes B.
        elif operator == '.':
            retval = lambda n, m=None, l=None: any(predicate(x, m, l)
                                                   for x in _immediately_after(n, df))
        # A , B       A immediately follows B.
        elif operator == ',':
            retval = lambda n, m=None, l=None: any(predicate(x, m, l)
                                                   for x in _immediately_before(n, df))
        # A .. B      A precedes B.
        elif operator == '..':
            retval = lambda n, m=None, l=None: any(predicate(x, m, l) for x in _after(n, df))
        # A ,, B      A follows B.
        elif operator == ',,':
            retval = lambda n, m=None, l=None: any(predicate(x, m, l) for x in _before(n, df))
        # A $ B       A is a sister of B (and A != B).
        elif operator == '$' or operator == '%':
            retval = lambda n, m=None, l=None: (has_governor(n) and
                                                any(predicate(x, m, l) for x in sisters(n, df)))
        # A $. B      A is a sister of and immediately precedes B.
        elif operator == '$.' or operator == '%.':
            raise NotImplementedError
            retval = lambda n, m=None, l=None: (hasattr(n, 'right_sibling') and
                                                bool(n.right_sibling()) and
                                                predicate(n.right_sibling(), m, l))
        # A $, B      A is a sister of and immediately follows B.
        elif operator == '$,' or operator == '%,':
            raise NotImplementedError
            retval = lambda n, m=None, l=None: (hasattr(n, 'left_sibling') and
                                                bool(n.left_sibling()) and
                                                predicate(n.left_sibling(), m, l))
        # A $.. B     A is a sister of and precedes B.
        elif operator == '$..' or operator == '%..':
            raise NotImplementedError
            retval = lambda n, m=None, l=None: (
                                                hasattr(n, 'parent_index') and
                                                has_governor(n) and
                                                any(predicate(x, m, l) for x in
                                                    governors(n, df)[n.parent_index() + 1:]))
        # A $,, B     A is a sister of and follows B.
        elif operator == '$,,' or operator == '%,,':
            raise NotImplementedError
            retval = lambda n, m=None, l=None: (
                                                hasattr(n, 'parent_index') and
                                                has_governor(n) and
                                                any(predicate(x, m, l) for x in
                                                    governors(n, df)[:n.parent_index()]))
        else:
            raise TgrepException(
                'cannot interpret tgrep operator "{0}"'.format(operator))
    # now return the built function
    if negated:
        return (lambda r: (lambda n, m=None, l=None: not r(n, m, l)))(retval)
    else:
        return retval

def _tgrep_conjunction_action(_s, _l, tokens, join_char = '&'):
    '''
    Builds a lambda function representing a predicate on a tree node
    from the conjunction of several other such lambda functions.

    This is prototypically called for expressions like
    (`tgrep_rel_conjunction`)::

        < NP & < AP < VP

    where tokens is a list of predicates representing the relations
    (`< NP`, `< AP`, and `< VP`), possibly with the character `&`
    included (as in the example here).

    This is also called for expressions like (`tgrep_node_expr2`)::

        NP < NN
        S=s < /NP/=n : s < /VP/=v : n .. v

    tokens[0] is a tgrep_expr predicate; tokens[1:] are an (optional)
    list of segmented patterns (`tgrep_expr_labeled`, processed by
    `_tgrep_segmented_pattern_action`).
    '''
    # filter out the ampersand
    tokens = [x for x in tokens if x != join_char]
    # print 'relation conjunction tokens: ', tokens
    if len(tokens) == 1:
        return tokens[0]
    else:
        return (lambda ts: lambda n, m=None, l=None: all(predicate(n, m, l)
                                                         for predicate in ts))(tokens)

def _tgrep_segmented_pattern_action(_s, _l, tokens):
    '''
    Builds a lambda function representing a segmented pattern.

    Called for expressions like (`tgrep_expr_labeled`)::

        =s .. =v < =n

    This is a segmented pattern, a tgrep2 expression which begins with
    a node label.

    The problem is that for segemented_pattern_action (': =v < =s'),
    the first element (in this case, =v) is specifically selected by
    virtue of matching a particular node in the tree; to retrieve
    the node, we need the label, not a lambda function.  For node
    labels inside a tgrep_node_expr, we need a lambda function which
    returns true if the node visited is the same as =v.

    We solve this by creating two copies of a node_label_use in the
    grammar; the label use inside a tgrep_expr_labeled has a separate
    parse action to the pred use inside a node_expr.  See
    `_tgrep_node_label_use_action` and
    `_tgrep_node_label_pred_use_action`.
    '''
    # tokens[0] is a string containing the node label
    node_label = tokens[0]
    # tokens[1:] is an (optional) list of predicates which must all
    # hold of the bound node
    reln_preds = tokens[1:]
    def pattern_segment_pred(n, m=None, l=None):
        '''This predicate function ignores its node argument.'''
        # look up the bound node using its label
        if l is None or node_label not in l:
            raise TgrepException('node_label ={0} not bound in pattern'.format(
                node_label))
        node = l[node_label]
        # match the relation predicates against the node
        return all(pred(node, m, l) for pred in reln_preds)
    return pattern_segment_pred

def _tgrep_node_label_use_action(_s, _l, tokens):
    '''
    Returns the node label used to begin a tgrep_expr_labeled.  See
    `_tgrep_segmented_pattern_action`.

    Called for expressions like (`tgrep_node_label_use`)::

        =s

    when they appear as the first element of a `tgrep_expr_labeled`
    expression (see `_tgrep_segmented_pattern_action`).

    It returns the node label.
    '''
    assert len(tokens) == 1
    assert tokens[0].startswith('=')
    return tokens[0][1:]

def _tgrep_node_label_pred_use_action(_s, _l, tokens):
    '''
    Builds a lambda function representing a predicate on a tree node
    which describes the use of a previously bound node label.

    Called for expressions like (`tgrep_node_label_use_pred`)::

        =s

    when they appear inside a tgrep_node_expr (for example, inside a
    relation).  The predicate returns true if and only if its node
    argument is identical the the node looked up in the node label
    dictionary using the node's label.
    '''
    assert len(tokens) == 1
    assert tokens[0].startswith('=')
    node_label = tokens[0][1:]
    def node_label_use_pred(n, m=None, l=None):
        # look up the bound node using its label
        if l is None or node_label not in l:
            raise TgrepException('node_label ={0} not bound in pattern'.format(
                node_label))
        node = l[node_label]
        # truth means the given node is this node
        return n is node
    return node_label_use_pred

def _tgrep_bind_node_label_action(_s, _l, tokens):
    '''
    Builds a lambda function representing a predicate on a tree node
    which can optionally bind a matching node into the tgrep2 string's
    label_dict.

    Called for expressions like (`tgrep_node_expr2`)::

        /NP/
        @NP=n
    '''
    # tokens[0] is a tgrep_node_expr
    if len(tokens) == 1:
        return tokens[0]
    else:
        # if present, tokens[1] is the character '=', and tokens[2] is
        # a tgrep_node_label, a string value containing the node label
        assert len(tokens) == 3
        assert tokens[1] == '='
        node_pred = tokens[0]
        node_label = tokens[2]
        def node_label_bind_pred(n, m=None, l=None):
            if node_pred(n, m, l):
                # bind `n` into the dictionary `l`
                if l is None:
                    raise TgrepException(
                        'cannot bind node_label {0}: label_dict is None'.format(
                            node_label))
                l[node_label] = n
                return True
            else:
                return False
        return node_label_bind_pred

def _tgrep_rel_disjunction_action(_s, _l, tokens):
    '''
    Builds a lambda function representing a predicate on a tree node
    from the disjunction of several other such lambda functions.
    '''
    # filter out the pipe
    tokens = [x for x in tokens if x != '|']
    # print 'relation disjunction tokens: ', tokens
    if len(tokens) == 1:
        return tokens[0]
    elif len(tokens) == 2:
        return (lambda a, b: lambda n, m=None, l=None:
                a(n, m, l) or b(n, m, l))(tokens[0], tokens[1])

def _macro_defn_action(_s, _l, tokens):
    '''
    Builds a dictionary structure which defines the given macro.
    '''
    assert len(tokens) == 3
    assert tokens[0] == '@'
    return {tokens[1]: tokens[2]}

def _tgrep_exprs_action(_s, _l, tokens):
    '''
    This is the top-level node in a tgrep2 search string; the
    predicate function it returns binds together all the state of a
    tgrep2 search string.

    Builds a lambda function representing a predicate on a tree node
    from the disjunction of several tgrep expressions.  Also handles
    macro definitions and macro name binding, and node label
    definitions and node label binding.
    '''
    if len(tokens) == 1:
        return lambda n, m=None, l=None: tokens[0](n, None, {})
    # filter out all the semicolons
    tokens = [x for x in tokens if x != ';']
    # collect all macro definitions
    macro_dict = {}
    macro_defs = [tok for tok in tokens if isinstance(tok, dict)]
    for macro_def in macro_defs:
        macro_dict.update(macro_def)
    # collect all tgrep expressions
    tgrep_exprs = [tok for tok in tokens if not isinstance(tok, dict)]
    # create a new scope for the node label dictionary
    def top_level_pred(n, m=macro_dict, l=None):
        label_dict = {}
        # bind macro definitions and OR together all tgrep_exprs
        return any(predicate(n, m, label_dict) for predicate in tgrep_exprs)
    return top_level_pred

def _build_tgrep_parser(set_parse_actions=True, df=False, case_sensitive=False):
    '''
    Builds a pyparsing-based parser object for tokenizing and
    interpreting tgrep search strings.
    '''
    tgrep_op = (pyparsing.Optional('!') +
                pyparsing.Regex('[$%,.<>=][%,.<>0-9-\':]*'))

    # todo: figure out how to actually do this
    w_tgrep_node_regex = pyparsing.QuotedString(quoteChar='w/', escChar='\\',
                                              unquoteResults=False, endQuoteChar="/")
    l_tgrep_node_regex = pyparsing.QuotedString(quoteChar='l/', escChar='\\',
                                              unquoteResults=False, endQuoteChar="/")
    e_tgrep_node_regex = pyparsing.QuotedString(quoteChar='e/', escChar='\\',
                                              unquoteResults=False, endQuoteChar="/")
    f_tgrep_node_regex = pyparsing.QuotedString(quoteChar='f/', escChar='\\',
                                              unquoteResults=False, endQuoteChar="/")
    p_tgrep_node_regex = pyparsing.QuotedString(quoteChar='p/', escChar='\\',
                                              unquoteResults=False, endQuoteChar="/")    
    tgrep_node_regex = pyparsing.QuotedString(quoteChar='/', escChar='\\',
                                              unquoteResults=False)
    w_tgrep_qstring = pyparsing.QuotedString(quoteChar='w"', escChar='\\',
                                           unquoteResults=False, endQuoteChar='"')
    l_tgrep_qstring = pyparsing.QuotedString(quoteChar='l"', escChar='\\',
                                           unquoteResults=False, endQuoteChar='"')
    e_tgrep_qstring = pyparsing.QuotedString(quoteChar='e"', escChar='\\',
                                           unquoteResults=False, endQuoteChar='"')
    f_tgrep_qstring = pyparsing.QuotedString(quoteChar='f"', escChar='\\',
                                           unquoteResults=False, endQuoteChar='"')
    p_tgrep_qstring = pyparsing.QuotedString(quoteChar='p"', escChar='\\',
                                           unquoteResults=False, endQuoteChar='"')
    tgrep_qstring = pyparsing.QuotedString(quoteChar='"', escChar='\\',
                                           unquoteResults=False, endQuoteChar='"')
    
    tgrep_qstring_icase = pyparsing.Regex(
        'i@\\"(?:[^"\\n\\r\\\\]|(?:\\\\.))*\\"')
    tgrep_node_regex_icase = pyparsing.Regex(
        'i@\\/(?:[^/\\n\\r\\\\]|(?:\\\\.))*\\/')
    tgrep_node_literal = pyparsing.Regex('[^][ \r\t\n;:.,&|<>()$!@%\'^=&]+')
    tgrep_expr = pyparsing.Forward()
    tgrep_relations = pyparsing.Forward()
    tgrep_parens = pyparsing.Literal('(') + tgrep_expr + ')'
    tgrep_nltk_tree_pos = (
        pyparsing.Literal('N(') +
        pyparsing.Optional(pyparsing.Word(pyparsing.nums) + ',' +
                           pyparsing.Optional(pyparsing.delimitedList(
                    pyparsing.Word(pyparsing.nums), delim=',') +
                                              pyparsing.Optional(','))) + ')')
    tgrep_node_label = pyparsing.Regex('[A-Za-z0-9]+')
    tgrep_node_label_use = pyparsing.Combine('=' + tgrep_node_label)
    # see _tgrep_segmented_pattern_action
    tgrep_node_label_use_pred = tgrep_node_label_use.copy()
    macro_name = pyparsing.Regex('[^];:.,&|<>()[$!@%\'^=\r\t\n ]+')
    macro_name.setWhitespaceChars('')
    macro_use = pyparsing.Combine('@' + macro_name)
    tgrep_node_expr = (tgrep_node_label_use_pred |
                       macro_use |
                       tgrep_nltk_tree_pos |
                       tgrep_qstring_icase |
                       tgrep_node_regex_icase |
                       w_tgrep_node_regex |
                       l_tgrep_node_regex |
                       e_tgrep_node_regex |
                       f_tgrep_node_regex |
                       p_tgrep_node_regex |
                       w_tgrep_qstring |
                       l_tgrep_qstring |
                       e_tgrep_qstring |
                       f_tgrep_qstring |
                       p_tgrep_qstring |
                       tgrep_qstring |
                       tgrep_node_regex |
                       '*' |
                       tgrep_node_literal)
    tgrep_node_expr2 = ((tgrep_node_expr +
                         pyparsing.Literal('=').setWhitespaceChars('') +
                         tgrep_node_label.copy().setWhitespaceChars('')) |
                        tgrep_node_expr)
    tgrep_node = (tgrep_parens |
                  (pyparsing.Optional("'") +
                   tgrep_node_expr2 +
                   pyparsing.ZeroOrMore("|" + tgrep_node_expr)))
    tgrep_brackets = pyparsing.Optional('!') + '[' + tgrep_relations + ']'
    tgrep_relation = tgrep_brackets | (tgrep_op + tgrep_node)
    tgrep_rel_conjunction = pyparsing.Forward()
    tgrep_rel_conjunction << (tgrep_relation +
                              pyparsing.ZeroOrMore(pyparsing.Optional('&') +
                                                   tgrep_rel_conjunction))
    tgrep_relations << tgrep_rel_conjunction + pyparsing.ZeroOrMore(
        "|" + tgrep_relations)
    tgrep_expr << tgrep_node + pyparsing.Optional(tgrep_relations)
    tgrep_expr_labeled = tgrep_node_label_use + pyparsing.Optional(tgrep_relations)
    tgrep_expr2 = tgrep_expr + pyparsing.ZeroOrMore(':' + tgrep_expr_labeled)
    macro_defn = (pyparsing.Literal('@') +
                  pyparsing.White().suppress() +
                  macro_name +
                  tgrep_expr2)
    tgrep_exprs = (pyparsing.Optional(macro_defn + pyparsing.ZeroOrMore(';' + macro_defn) + ';') +
                   tgrep_expr2 +
                   pyparsing.ZeroOrMore(';' + (macro_defn | tgrep_expr2)) +
                   pyparsing.ZeroOrMore(';').suppress())
    if set_parse_actions:
        tgrep_node_label_use.setParseAction(_tgrep_node_label_use_action)
        tgrep_node_label_use_pred.setParseAction(_tgrep_node_label_pred_use_action)
        macro_use.setParseAction(_tgrep_macro_use_action)
        tgrep_node.setParseAction(lambda x,y,z: _tgrep_node_action(x, y, z,
                                                 case_sensitive=case_sensitive))
        tgrep_node_expr2.setParseAction(_tgrep_bind_node_label_action)
        tgrep_parens.setParseAction(_tgrep_parens_action)
        tgrep_nltk_tree_pos.setParseAction(_tgrep_nltk_tree_pos_action)
        tgrep_relation.setParseAction(lambda x,y,z: _tgrep_relation_action(x, y, z, df=df))
        tgrep_rel_conjunction.setParseAction(_tgrep_conjunction_action)
        tgrep_relations.setParseAction(_tgrep_rel_disjunction_action)
        macro_defn.setParseAction(_macro_defn_action)
        # the whole expression is also the conjunction of two
        # predicates: the first node predicate, and the remaining
        # relation predicates
        tgrep_expr.setParseAction(_tgrep_conjunction_action)
        tgrep_expr_labeled.setParseAction(_tgrep_segmented_pattern_action)
        tgrep_expr2.setParseAction(functools.partial(_tgrep_conjunction_action,
                                                     join_char = ':'))
        tgrep_exprs.setParseAction(_tgrep_exprs_action)
    return tgrep_exprs.ignore('#' + pyparsing.restOfLine)

def depgrep_compile(depgrep_string, df=False, case_sensitive=False):
    '''
    Parses (and tokenizes, if necessary) a TGrep search string into a
    lambda function.
    '''
    parser = _build_tgrep_parser(True, df=df, case_sensitive=case_sensitive)
    if isinstance(depgrep_string, bytes):
        depgrep_string = depgrep_string.decode()
    return list(parser.parseString(depgrep_string, parseAll=True))[0]

def depgrep(data, compiled_depgrep, case_sensitive=False, df=False):
    '''
    Run a query string over data, returning matching tokens
    '''
    from corpkit.constants import CONLL_COLUMNS

    match_ixs = []

    data = data[CONLL_COLUMNS[1:]]

    matches = data.apply(compiled_depgrep, axis=1)
    if matches.dtypes.name == 'bool':
        return df.loc[matches]
    else:
        import numpy as np
        matches = matches.fillna(value=np.nan)
        return df.loc[matches.dropna().index]
