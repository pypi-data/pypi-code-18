import utopia.tools.eutils

from lxml import etree

def fetch(pmcid):
    return utopia.tools.eutils.efetch(id=pmcid, db='pmc')

def search(title):
    data = []
    # FIXME How best to search PMC for a title?
    return data

def identify(id, id_type):
    results = utopia.tools.eutils.esearch(term='"{0}"[{1}]'.format(id, id_type.upper()), db='pmc', retmax=1)
    parser = etree.XMLParser(ns_clean=True, recover=True)
    ids = etree.fromstring(results, parser).xpath('//Id')
    if len(ids) == 1:
        pmcid = ids[0].text.upper()
        if not pmcid.startswith('PMC'):
            pmcid = 'PMC{}'.format(pmcid)
        return pmcid
