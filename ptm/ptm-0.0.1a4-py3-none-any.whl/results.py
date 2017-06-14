"""
Module contains class to get results.
To fech results used BeautifulSoup.
"""
from functools import reduce
from operator import xor

class ResultAction: #pylint: disable-msg=R0903
    """
    Base class for describing action of get result.
    """
    def __init__(self, *args, **kwargs):
        """
        Initial.
            HTML block description
            ----------------------
            Use arguments and named arguments to find_all() method from BeautifulSoup.
            args -> Argumnets for find_all(), like as html block name - 'a', 'div' and etc;
            kwargs -> Named arguments for find_all(), like as "attrs={'class': 'some_css_class'}";
        """
        self.args = args
        self.kwargs = kwargs

class gtexts(ResultAction): #pylint: disable-msg=R0903,C0103
    """
    Class for decribing action of get text from BeautifulSoup Tag.
    """
    def __init__(self, *args, **kwargs):
        """
        Initial of super initial.
        """
        super().__init__(*args, **kwargs)

    def __call__(self, parent_tag, key):
        """
        Run action.
        Input:
            parent_tag -> BeautifulSoup Tag;
        Output:
            list_of_text -> List of texts from BeautifulSoup Tags;
        """
        return {key: [tag.get_text().strip() for tag in parent_tag.find_all(*self.args, **self.kwargs)]}

class gattrs(ResultAction): #pylint: disable-msg=R0903,C0103
    """
    Class for describing action of get attributes from BeautifulSoup Tag.
    """
    def __init__(self, *args, target_attribute='alt', **kwargs):
        """
        Initial of super initial.
        Added target atribute.
        Input:
            target_attribute -> Target attribute;
        """
        super().__init__(*args, **kwargs)
        self.target_attribute = target_attribute

    def __call__(self, parent_tag, key=None):
        """
        Run action.
        Input:
            parent_tag -> Parent BeautifulSoup Tag;
        Output:
            list_of_attributes -> List of value of atributes;
        """
        return {key: [tag[self.target_attribute]
                for tag in parent_tag.find_all(*self.args, **self.kwargs)]}

class KeysRealtions: #pylint: disable-msg=R0903
    """
    Class for describing relations of keys.
    """
    def __init__(self, relations):
        self.relations = relations

    def __hash__(self):
        return reduce(xor, self.relations.values().sort())

class KeyValue: #pylint: disable-msg=R0903
    """
    Class to describig key-value relations.
    """
    def __init__(self, keys_action, values_action):
        self.keys_action = keys_action
        self.values_action = values_action

    def __call__(self, parent_tag, keys_relations):
        relations = keys_relations.relations
        return {relations[key]: value for key, value in zip(self.keys_action(parent_tag, 'key')['key'], self.values_action(parent_tag, 'key')['key']) if key in relations.keys()}
