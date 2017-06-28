
class BaseObject(object):
    "base object for shared functions"
    def __unicode__(self):
        """
        Return unicode representation of the simple object properties,
        if there is a list or dict just return an empty representation
        for easier viewing and test case scenario writing
        """
        unicode_dict = {}
        for k in self.__dict__:
            if type(self.__dict__.get(k)) == list:
                unicode_dict[k] = []
            elif type(self.__dict__.get(k)) == dict:
                unicode_dict[k] = {}
            else:
                unicode_dict[k] = unicode(self.__dict__.get(k))
        return unicode(unicode_dict)

class Article(BaseObject):
    """
    We include some boiler plate in the init, namely article_type
    """
    contributors = []

    def __new__(cls, doi=None, title=None):
        new_instance = object.__new__(cls)
        new_instance.init(doi, title)
        return new_instance

    def init(self, doi=None, title=None):
        self.article_type = "research-article"
        self.display_channel = None
        self.doi = doi
        self.contributors = []
        self.title = title
        self.abstract = ""
        self.research_organisms = []
        self.manuscript = None
        self.dates = None
        self.license = None
        self.article_categories = []
        self.conflict_default = None
        self.ethics = []
        self.author_keywords = []
        self.funding_awards = []
        self.ref_list = []
        self.component_list = []
        # For PubMed function a hook to specify if article was ever through PoA pipeline
        self.was_ever_poa = None
        self.is_poa = None
        self.volume = None
        self.elocation_id = None
        self.related_articles = []
        self.version = None
        self.datasets = []
        self.funding_awards = []
        self.funding_note = None

    def add_contributor(self, contributor):
        self.contributors.append(contributor)

    def add_research_organism(self, research_organism):
        self.research_organisms.append(research_organism)

    def add_date(self, date):
        if not self.dates:
            self.dates = {}
        self.dates[date.date_type] = date

    def get_date(self, date_type):
        try:
            return self.dates[date_type]
        except (KeyError, TypeError):
            return None

    def get_display_channel(self):
        # display-channel string partly relates to the articleType
        return self.display_channel

    def add_article_category(self, article_category):
        self.article_categories.append(article_category)

    def has_contributor_conflict(self):
        # Return True if any contributors have a conflict
        for contributor in self.contributors:
            if contributor.conflict:
                return True
        return False

    def add_ethic(self, ethic):
        self.ethics.append(ethic)

    def add_author_keyword(self, author_keyword):
        self.author_keywords.append(author_keyword)

    def add_dataset(self, dataset):
        self.datasets.append(dataset)

    def get_datasets(self, dataset_type=None):
        if dataset_type:
            return [d for d in self.datasets if d.dataset_type == dataset_type]
        else:
            return self.datasets

    def add_funding_award(self, funding_award):
        self.funding_awards.append(funding_award)


class ArticleDate(BaseObject):
    """
    A struct_time date and a date_type
    """
    def __new__(cls, date_type, date):
        new_instance = object.__new__(cls)
        new_instance.init(date_type, date)
        return new_instance

    def init(self, date_type, date):
        self.date_type = date_type
        # Date as a time.struct_time
        self.date = date


class Contributor(BaseObject):
    """
    Currently we are not sure that we can get an auth_id for
    all contributors, so this attribute remains an optional attribute.
    """

    corresp = False
    equal_contrib = False

    auth_id = None
    orcid = None
    collab = None
    conflict = None
    group_author_key = None

    def __new__(cls, contrib_type, surname, given_name, collab=None):
        new_instance = object.__new__(cls)
        new_instance.init(contrib_type, surname, given_name, collab)
        return new_instance

    def init(self, contrib_type, surname, given_name, collab=None):
        self.contrib_type = contrib_type
        self.surname = surname
        self.given_name = given_name
        self.affiliations = []
        self.collab = collab

    def set_affiliation(self, affiliation):
        self.affiliations.append(affiliation)

    def set_conflict(self, conflict):
        self.conflict = conflict


class Affiliation(BaseObject):
    phone = None
    fax = None
    email = None
    department = None
    institution = None
    city = None
    country = None
    text = None

    def __new__(cls):
        new_instance = object.__new__(cls)
        new_instance.init()
        return new_instance

    def init(self):
        pass


class Dataset(BaseObject):
    """
    Article component representing a dataset
    """
    def __new__(cls):
        new_instance = object.__new__(cls)
        new_instance.init()
        return new_instance

    def init(self):
        self.dataset_type = None
        self.authors = []
        self.source_id = None
        self.year = None
        self.title = None
        self.license_info = None

    def add_author(self, author):
        self.authors.append(author)


class FundingAward(BaseObject):
    """
    An award group as part of a funding group
    """
    def __new__(cls):
        new_instance = object.__new__(cls)
        new_instance.init()
        return new_instance

    def init(self):
        self.award_ids = []
        self.institution_name = None
        self.institution_id = None
        self.principal_award_recipients = []

    def add_award_id(self, award_id):
        self.award_ids.append(award_id)

    def add_principal_award_recipient(self, contributor):
        # Accepts an instance of Contributor
        self.principal_award_recipients.append(contributor)

    def get_funder_identifier(self):
        # Funder identifier is the unique id found in the institution_id DOI
        try:
            return self.institution_id.split('/')[-1]
        except:
            return None

    def get_funder_name(self):
        # Alias for institution_name parsed from the XML
        return self.institution_name


class License(BaseObject):
    """
    License with some preset values by license_id
    """

    license_id = None
    license_type = None
    copyright = False
    href = None
    name = None
    p1 = None
    p2 = None

    def __new__(cls, license_id=None):
        new_instance = object.__new__(cls)
        new_instance.init(license_id)
        return new_instance

    def init(self, license_id):
        if license_id:
            self.init_by_license_id(license_id)

    def init_by_license_id(self, license_id):
        """
        For license_id value, set the license properties
        """
        if int(license_id) == 1:
            self.license_id = license_id
            self.license_type = "open-access"
            self.copyright = True
            self.href = "http://creativecommons.org/licenses/by/4.0/"
            self.name = "Creative Commons Attribution License"
            self.p1 = "This article is distributed under the terms of the "
            self.p2 = (" permitting unrestricted use and redistribution provided that the " +
                       "original author and source are credited.")
        elif int(license_id) == 2:
            self.license_id = license_id
            self.license_type = "open-access"
            self.copyright = False
            self.href = "http://creativecommons.org/publicdomain/zero/1.0/"
            self.name = "Creative Commons CC0"
            self.p1 = ("This is an open-access article, free of all copyright, and may be " +
                       "freely reproduced, distributed, transmitted, modified, built upon, or " +
                       "otherwise used by anyone for any lawful purpose. The work is made " +
                       "available under the ")
            self.p2 = " public domain dedication."


class Citation(BaseObject):
    """
    A ref or citation in the article to support crossref VOR deposits initially
    """
    def __new__(cls):
        new_instance = object.__new__(cls)
        new_instance.init()
        return new_instance

    def init(self):
        self.publication_type = None
        self.authors = []
        # For journals
        self.article_title = None
        self.source = None
        self.volume = None
        self.fpage = None
        self.lpage = None
        self.elocation_id = None
        self.doi = None
        self.year = None
        # For books
        self.volume_title = None

    def add_author(self, author):
        # Author is a dict of values
        self.authors.append(author)

    def get_journal_title(self):
        # Alias for source
        return self.source


class Component(BaseObject):
    """
    An article component with a component DOI, primarily for crossref VOR deposits
    """
    def __new__(cls):
        new_instance = object.__new__(cls)
        new_instance.init()
        return new_instance

    def init(self):
        self.title = None
        self.subtitle = None
        self.mime_type = None
        self.doi = None
        self.doi_resource = None
        self.permissions = None


class RelatedArticle(BaseObject):
    """
    Related article tag data as an object
    """
    def __new__(cls):
        new_instance = object.__new__(cls)
        new_instance.init()
        return new_instance

    def init(self):
        self.xlink_href = None
        self.related_article_type = None
        self.ext_link_type = None
