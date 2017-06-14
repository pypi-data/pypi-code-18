import pandas as pd
import string
import textcounts
def test_core():
    test_list = pd.Series(["this is a test", "THIS IS A TEST", "This is a Test"])

    assert textcounts.prop_mentions(test_list, ["test", "this"]) == 1
    assert textcounts.prop_mentions(test_list, ["test"]) == 1
    assert textcounts.prop_mentions(test_list, ["test"], exclude="a test") == 0
    assert textcounts.prop_mentions(test_list, ["test", "this"], exclude="a test") == 1

def test_pp_find_mentions():

    with open('examples/pp.txt','r') as f:
        s = f.read()
    
    pp_pars = []
    for item in s.split("\n\n"):
        if item != '' or item not in string.punctuation:
            pp_pars.append(item.replace("\n", " "))


    de_list = textcounts.find_mentions(pp_pars, "darcy")
    assert len(de_list) == 347

def text_pp_pattern_counts():
    with open('examples/pp.txt','r') as f:
        s = f.read()

    pp_pars = []
    for item in s.split("\n\n"):
        if item != '' or item not in string.punctuation:
            pp_pars.append(item.replace("\n", " "))

    assert textcounts.pattern_counts(pp_pars, ["she", "her", "mrs"]).sum().sum() == 6625