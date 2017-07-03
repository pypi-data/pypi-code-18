import requests
import json

DC_PRODUCTION_URL = "https://dc.directchannel.it/mentor/api"
DC_TEST_URL = "http://test.directchannel.it/mentor/api"


class RequestWrapper(object):

    def _send_request(self, url, payload, headers, method="POST"):
        try:
            return requests.request(method, url=url, data=json.dumps(payload, ensure_ascii=False), headers=headers)
        except requests.exceptions.RequestException as e:
            return {
                "result": "KO",
                "message": "SERVER ERROR {0}".format(str(e)),
                "data": "",
            }

    def _handle_data(self, data):
        if hasattr(data, 'text'):
            return json.loads(data.text)
        else:
            return data


class DirectChannel(RequestWrapper):
    url = None
    env = None
    application = None
    token = None
    user = None

    def __init__(self, env, application, token, user, test=False):
        self.url = DC_PRODUCTION_URL if not test else DC_TEST_URL
        self.env = env
        self.application = application
        self.token = token
        self.user = user

    def wsc_table(self, param):
        payload = {
            "env": self.env,
            "application": self.application,
            "operation": "get",
            "token": self.token,
            "user": self.user,
            "param": param,
            "data": None
        }
        headers = {'content-type': 'application/json'}
        url = "{0}/{1}".format(self.url, 'wsc_table.ashx')
        return self._handle_data(self._send_request(url=url, method="GET", payload=payload, headers=headers))

    def wsc_save_donor(self, codice=None, codiceorigine=None, codiceweb=None, tipo=None, sottotipo=None, nome=None,
                       cognome=None, ragionesociale=None, genere=None, datanascita=None, luogonascita=None,
                       codicefiscale=None, partitaiva=None, email1=None, email2=None, telefono1=None, telefono2=None,
                       cellulare1=None, cellulare2=None, presso=None, dug=None, duf=None, civico=None, altrocivico=None,
                       frazione=None, localita=None, provincia=None, cap=None, codicenazione=None, codicecampagna=None):
        payload = {
            "env": self.env,
            "application": self.application,
            "operation": "save",
            "token": self.token,
            "user": self.user,
            "param": "",
            "data": {
                "codice": codice,
                "codiceOrigine": codiceorigine,
                "codiceWeb": codiceweb,
                "tipo": tipo,
                "sottotipo": sottotipo,
                "nome": nome,
                "cognome": cognome,
                "ragioneSociale": ragionesociale,
                "genere": genere,
                "dataNascita": datanascita,
                "luogoNascita": luogonascita,
                "codiceFiscale": codicefiscale,
                "partitaIVA": partitaiva,
                "email1": email1,
                "email2": email2,
                "telefono1": telefono1,
                "telefono2": telefono2,
                "cellulare1": cellulare1,
                "cellulare2": cellulare2,
                "presso": presso,
                "dug": dug,
                "duf": duf,
                "civico": civico,
                "altroCivico": altrocivico,
                "frazione": frazione,
                "localita": localita,
                "provincia": provincia,
                "cap": cap,
                "codiceNazione": codicenazione,
                "codiceCampagna": codicecampagna
            }
        }
        headers = {'content-type': 'application/json'}
        url = "{0}/{1}".format(self.url, 'wsc_save_donor.ashx')
        return self._handle_data(self._send_request(url=url, payload=payload, headers=headers))

    def wsc_save_donation(self, idregolare=None, codicedonatore=None, codicecampagna=None, codicecentro=None,
                          codicebambino=None, codiceprogetto=None, codicecanale=None, importo=None, metodo=None,
                          dataoperazione=None,
                          datavaluta=None, codicetransizione=None, idweb=None, note=None):
        payload = {
            "env": self.env,
            "application": self.application,
            "operation": "save",
            "token": self.token,
            "user": self.user,
            "param": "",
            "data": {
                "idRegolare": idregolare,
                "codiceDonatore": codicedonatore,
                "codiceCampagna": codicecampagna,
                "codiceCentro": codicecentro,
                "codiceBambino": codicebambino,
                "codiceProgetto": codiceprogetto,
                "codiceCanale": codicecanale,
                "importo": importo,
                "metodo": metodo,
                "dataOperazione": dataoperazione,
                "dataValuta": datavaluta,
                "codiceTransazione": codicetransizione,
                "idWeb": idweb,
                "note": note
            }
        }
        headers = {'content-type': 'application/json'}
        url = "{0}/{1}".format(self.url, 'wsc_save_donation.ashx')
        return self._handle_data(self._send_request(url=url, payload=payload, headers=headers))

    def wsc_save_product(self, iddonazione=None, codiceprodotto=None, quantita=None, prezzounitario=None):
        payload = {
            "env": self.env,
            "application": self.application,
            "operation": "save",
            "token": self.token,
            "user": self.user,
            "param": "",
            "data": {
                "idDonazione": iddonazione,
                "codiceProdotto": codiceprodotto,
                "quantita": quantita,
                "prezzoUnitario": prezzounitario
            }
        }
        headers = {'content-type': 'application/json'}
        url = "{0}/{1}".format(self.url, 'wsc_save_product.ashx')
        return self._handle_data(self._send_request(url=url, payload=payload, headers=headers))

    def wsc_save_regular(self, id=None, generasostegno=None, codicedonatore=None, codicecampagna=None, codicecentro=None,
                         codicebambino=None, codiceprogetto=None, codicecanale=None, importo=None, frequenza=None,
                         metodo=None, iban=None, urn=None, lotto=None, locazione=None, cittalocazione=None,
                         preferenzagenere=None, preferenzaetaminima=None, preferenzaetamassima=None, note=None ):
        payload = {
            "env": self.env,
            "application": self.application,
            "operation": "save",
            "token": self.token,
            "user": self.user,
            "param": "",
            "data": {
                "ID": id,
                "generaSostegno": generasostegno,
                "codiceDonatore": codicedonatore,
                "codiceCampagna": codicecampagna,
                "codiceCentro": codicecentro,
                "codiceBambino": codicebambino,
                "codiceProgetto": codiceprogetto,
                "codiceCanale": codicecanale,
                "importo": importo,
                "frequenza": frequenza,
                "metodo": metodo,
                "IBAN": iban,
                "urn": urn,
                "lotto": lotto,
                "locazione": locazione,
                "cittaLocazione": cittalocazione,
                "preferenzaGenere": preferenzagenere,
                "preferenzaEtaMinima": preferenzaetaminima,
                "preferenzaEtaMassima": preferenzaetamassima,
                "note": note
            }
        }

        headers = {'content-type': 'application/json'}
        url = "{0}/{1}".format(self.url, 'wsc_save_regular.ashx')
        return self._handle_data(self._send_request(url=url, payload=payload, headers=headers))

    def wsc_save_activity(self, codicedonatore=None, codicecampagna=None, codicebambino=None, codiceprogetto=None,
                          codicecanale=None, idregolare=None, tipo=None, sottotipo=None,
                          oggetto=None, note=None, utenteassegnatario=None, gruppoutentiassegnatario=None,
                          stato=None):
        payload = {
            "env": self.env,
            "application": self.application,
            "operation": "save",
            "token": self.token,
            "user": self.user,
            "param": "",
            "data": {
                "codiceDonatore": codicedonatore,
                "codiceCampagna": codicecampagna,
                "codiceBambino": codicebambino,
                "codiceProgetto": codiceprogetto,
                "codiceCanale": codicecanale,
                "idRegolare": idregolare,
                "tipo": tipo,
                "sottotipo": sottotipo,
                "oggetto": oggetto,
                "note": note,
                "utenteAssegnatario": utenteassegnatario,
                "gruppoUtentiAssegnatario": gruppoutentiassegnatario,
                "stato": stato
            }
        }
        headers = {'content-type': 'application/json'}
        url = "{0}/{1}".format(self.url, 'wsc_save_activity.ashx')
        return self._handle_data(self._send_request(url=url, payload=payload, headers=headers))

    def wsc_save_privacy(self, codicedonatore, codiceprivacy, attiva, dataentata, datauscita, note):
        payload = {
            "env": self.env,
            "application": self.application,
            "operation": "save",
            "token": self.token,
            "user": self.user,
            "param": "",
            "data": {
                "codiceDonatore": codicedonatore,
                "codicePrivacy": codiceprivacy ,
                "attiva": attiva,
                "dataEntata": dataentata,
                "dataUscita": datauscita,
                "note": note
            }
        }
        headers = {'content-type': 'application/json'}
        url = "{0}/{1}".format(self.url, 'wsc_save_privacy.ashx')
        return self._handle_data(self._send_request(url=url, payload=payload, headers=headers))

    def wsc_get_children(self, codicebambino):
        payload = {
            "env": self.env,
            "application": self.application,
            "operation": "get",
            "token": self.token,
            "user": self.user,
            "param": codicebambino,
            "data": None
        }
        headers = {'content-type': 'application/json'}
        url = "{0}/{1}".format(self.url, 'wsc_get_children.ashx')
        return self._handle_data(self._send_request(url=url, method="GET", payload=payload, headers=headers))
