import requests

domain = 'https://run.mydaco.com'

def call(endpointToken, parameters):
  r = requests.post(domain, json = {'externalId':externalId, 'parameters':parameters})
  return r.json()

def setDomain(dom):
  global domain
  domain = dom
