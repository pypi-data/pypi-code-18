from ontobio.io.entityparser import GpiParser
from ontobio.assoc_factory import AssociationSetFactory
from ontobio.ontol_factory import OntologyFactory

ONT = "tests/resources/go-truncated-pombase.json"
GPI = "tests/resources/truncated-mgi.gpi"
    
def test_parse_gpi():
    ont = OntologyFactory().create(ONT)
    p = GpiParser()
    results = p.parse(open(GPI,"r"))
    for r in results:
        print(r)
    r1 = results[0]
    assert r1['label'] == 'a'
    assert r1['full_name'] == 'nonagouti'
    
    for m in p.report.messages:
        print("MESSAGE: {}".format(m))
    assert len(p.report.messages) == 0
    print(p.report.to_markdown())
    
    
