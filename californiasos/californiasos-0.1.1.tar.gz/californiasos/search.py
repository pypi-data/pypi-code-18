import requests
import datetime

from http import cookies
from urllib.parse import urlencode
from requests.utils import dict_from_cookiejar, cookiejar_from_dict
from bs4 import BeautifulSoup


GOOGLE_CAPITAL_MANAGEMENT_COMPANY_LLC_ENTITY_ID = "201332210398"

class CaliforniaEntitySearchResult:
    def __init__(self, entities):
        self.entities = entities

class CaliforniaEntitySearchEntity:
    def __init__(self, entity_number, registration_date, status, entity_name, juristdiction, agent_name):
        self.entity_number = entity_number
        self.registration_date = registration_date
        self.status = status
        self.entity_name = entity_name
        self.juristdiction = juristdiction
        self.agent_name = agent_name

class CaliforniaEntityDetail:
    def __init__(self, entity_number, registration_date, juristdiction, entity_type, status, agent_name, entity_address, entity_mailing_address, docs):
        self.entity_number = entity_number
        self.registration_date = registration_date
        self.juristdiction = juristdiction
        self.entity_type = entity_type
        self.status = status
        self.agent_name = agent_name
        self.entity_address = entity_address
        self.entity_mailing_address = entity_mailing_address
        self.docs = docs

class CaliforniaEntityDocument:
    def __init__(self, name, date):
        self.name = name
        self.date = date

class MultipleEntityException(Exception):
    pass

class CaliforniaSOS:
    def __init__(self, base_url = "https://businesssearch.sos.ca.gov"):
        self.base_url = base_url
        self.session = requests.Session()
        self.csrf_token = None

    def _must_get_csrf_token(self):
        # Just perform any search so we get the session token in the cookie jar and a CSRF token
        self.search_by_entity_id(GOOGLE_CAPITAL_MANAGEMENT_COMPANY_LLC_ENTITY_ID)

    def _extract_cookies(self, response):
        if "Set-Cookie" not in response.headers:
            return

        for setcookie in response.headers["Set-Cookie"].split(", "):
            cookie = cookies.BaseCookie()
            cookie.load(setcookie)
            for (key, morsel) in cookie.items():
                self.session.cookies.set(morsel.key, morsel.value)

    def _extract_csrf_token(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        searchResults = soup.find(id="formSearchResults")
        if searchResults is None:
            return
        inputs = searchResults.find_all("input")
        if inputs is None or len(inputs) == 0:
            return
        self.csrf_token = inputs[0]["value"]
    
    def search_by_entity_id(self, entity_id):
        params = {"SearchType": "NUMBER",
                  "SearchCriteria": entity_id}
        referer_params = urlencode(params)
        referer = self.base_url + "/CBS/SearchResults?" + referer_params
        headers = {"Referer": referer}
        result = self.session.get(self.base_url + "/CBS/SearchResults", params=params, headers=headers)

        self._extract_csrf_token(result)
        self._extract_cookies(result)

        soup = BeautifulSoup(result.text, "html.parser")
        html_entities = soup.find(id="enitityTable").tbody.find_all("tr")
        if len(html_entities) > 1:
            raise MultipleEntityException()
        columns = html_entities[0].find_all("td")
        text_columns = []
        for column in columns:
            text_columns.append("".join([text for text in column.stripped_strings]))
        entity_number = text_columns[0]
        registration_date = text_columns[1]
        status = text_columns[2]
        entity_name = columns[3].button.get_text()
        juristdiction = text_columns[4]
        agent_name = text_columns[5]

        registration_date_date = datetime.datetime.strptime(registration_date, "%m/%d/%Y").date()

        entity = CaliforniaEntitySearchEntity(entity_number = entity_number,
                                              registration_date = registration_date_date,
                                              status = status,
                                              entity_name = entity_name,
                                              juristdiction = juristdiction,
                                              agent_name = agent_name)
            
        return CaliforniaEntitySearchResult(entities=[entity])

    def get_entity_documents(self, entity_id):
        self._must_get_csrf_token()

        data = {"__RequestVerificationToken": self.csrf_token,
                "EntityId": entity_id}
        result = self.session.post(self.base_url + "/CBS/Detail", data=data)
        soup = BeautifulSoup(result.text, "html.parser")

        # details_html = soup.find(id="formDetails").find_all("div", attrs={"class": "row"})
        docs_html = soup.find(id="docTable").tbody.find_all("tr")
        docs = []
        for doc in docs_html:
            columns = doc.find_all("td")
            text_columns = []
            for column in columns:
                text_columns.append("".join([text for text in column.stripped_strings]))
            document_name = text_columns[0]
            document_date_string = text_columns[1]
            document_date = datetime.datetime.strptime(document_date_string, "%m/%d/%Y").date()
            document = CaliforniaEntityDocument(document_name, document_date)
            docs.append(document)
        return docs
