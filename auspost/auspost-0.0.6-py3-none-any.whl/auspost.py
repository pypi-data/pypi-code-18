
"""
Copyright 2017 James Hodgkinson

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

try:
    from collections import namedtuple
    from mechanicalsoup import StatefulBrowser
except ImportError as e:
    importmessage = "Failure while loading auspost module's dependencies: {}".format(e)
    raise ImportError(importmessage)

AusPostData = namedtuple('AusPostData', ['postcode', 'suburb', 'state'])

def search_postcode(searchterm : str):
    """ this does a search against the Australia Post site to 
    grab postcode/suburb/state data and returns a namedtuple 
    AusPostData(postcode=int, suburb=str, state=str)
    """
    browser = StatefulBrowser(soup_config={'features': 'lxml'})
    # Uncomment for a more verbose output:
    # browser.set_verbose(2)

    # build the URL for search
    searchurl = "http://auspost.com.au/postcode/{}".format(searchterm.replace(' ', '%20'))

    # grab the page
    try:
        browser.open(searchurl)
    except:
        raise ConnectionError("Failed to open the url '{}'".format(searchurl))
    # get the page contents
    page = browser.get_current_page()

    # find the ol
    ols = page.find_all('ol')
    if ols:
        # find the lis within the ol
        lis = ols[0].find_all('li')
        # pull out the data
        for li in lis:
            # this is in the li tag
            if 'id="result' in str(li):
                # this is the data found in June 2017
                #<span class="suburb-map-postcode">POSTCODE</span>
                #<h2>SUBURB, STATE</h2>
                postcode = li.find_all('span')
                if postcode:
                    postcode = postcode[0].contents[0]
                    secondfield = li.find_all('h2')
                    if secondfield:
                        suburb, state = secondfield[0].contents[0].split(",")
                        suburb, state = suburb.strip(), state.strip()
                        if postcode and state and suburb:
                            yield AusPostData(postcode=int(postcode), state=state, suburb=suburb)
