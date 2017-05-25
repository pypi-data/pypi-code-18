import clarus.services

def domain(output=None, **params):
    return clarus.services.api_request('Util', 'Domain', output=output, **params)

def fixingdates(output=None, **params):
    return clarus.services.api_request('Util', 'FixingDates', output=output, **params)

def fxforwarddate(output=None, **params):
    return clarus.services.api_request('Util', 'FxForwardDate', output=output, **params)

def fxoptiondate(output=None, **params):
    return clarus.services.api_request('Util', 'FxOptionDate', output=output, **params)

def fxspotdate(output=None, **params):
    return clarus.services.api_request('Util', 'FxSpotDate', output=output, **params)

def grid(output=None, **params):
    return clarus.services.api_request('Util', 'Grid', output=output, **params)

def irdspotdate(output=None, **params):
    return clarus.services.api_request('Util', 'IrdSpotDate', output=output, **params)

def periodlength(output=None, **params):
    return clarus.services.api_request('Util', 'PeriodLength', output=output, **params)

def tickers(output=None, **params):
    return clarus.services.api_request('Util', 'Tickers', output=output, **params)

