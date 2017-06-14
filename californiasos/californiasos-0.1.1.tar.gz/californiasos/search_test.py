import datetime
import vcr

from .search import CaliforniaSOS, CaliforniaEntitySearchEntity, CaliforniaEntityDocument, CaliforniaEntitySearchResult
my_vcr = vcr.VCR(cassette_library_dir='fixtures/cassettes')

qubit_id = "201501310067"

@my_vcr.use_cassette()
def test_qubit_search():
    s = CaliforniaSOS()
    results = s.search_by_entity_id(qubit_id)
    assert isinstance(results, CaliforniaEntitySearchResult)
    assert len(results.entities) == 1
    assert isinstance(results.entities[0], CaliforniaEntitySearchEntity)
    qubit = results.entities[0]
    assert qubit.entity_number == qubit_id
    assert qubit.registration_date == datetime.date(2015, 1, 8)
    assert qubit.status == "ACTIVE"
    assert qubit.entity_name == "QUBIT, LLC"
    assert qubit.juristdiction == "CALIFORNIA"
    assert qubit.agent_name == "JACOB GREENLEAF"

@my_vcr.use_cassette()
def test_qubit_documents():
    s = CaliforniaSOS()
    docs = s.get_entity_documents(qubit_id)
    print(docs)
    assert len(docs) == 3
    assert isinstance(docs[0], CaliforniaEntityDocument)
    assert docs[0].name == "REGISTRATION"
    assert docs[0].date == datetime.date(2015, 1, 8)
    assert isinstance(docs[0], CaliforniaEntityDocument)
    assert docs[1].name == "SI-COMPLETE"
    assert docs[1].date == datetime.date(2015, 7, 1)
    assert isinstance(docs[1], CaliforniaEntityDocument)
    assert docs[2].name == "SI-COMPLETE"
    assert docs[2].date == datetime.date(2017, 4, 19)
