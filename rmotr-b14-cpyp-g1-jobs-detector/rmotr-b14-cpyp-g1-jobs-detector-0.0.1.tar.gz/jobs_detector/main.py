import click
import requests
from bs4 import BeautifulSoup

from jobs_detector import settings

DEFAULT_KEYWORDS = [
    # set some default keywords here
    'Remote',
    'Postgres',
    'Python',
    'Javascript',
    'React',
    'Pandas'
]


@click.group()
def jobs_detector():
    pass


@jobs_detector.command()
@click.option('-i', '--post-id', type=str, required=True)
@click.option('-k', '--keywords', type=str, default=','.join(DEFAULT_KEYWORDS))
@click.option('-c', '--combinations', type=str,
              callback=lambda _, __, x: x.split(',') if x else x)
def hacker_news(post_id, keywords, combinations):
    """
    This subcommand aims to get jobs statistics by parsing "who is hiring?"
    HackerNews posts based on given set of keywords.
    """
    # HINT: You will probably want to use the `BeautifulSoup` tool to
    # parse the HTML content of the website
    
    keywords = keywords.split(",")
    kw_counter = {}
    for kw in keywords:
        kw_counter[kw] = 0 
    
    if combinations:
        #combinations = combinations.split(",")
        #print(combinations)
        comb_counter = {}
        for c in combinations:
            comb_counter[c] = 0 
        
    jobs_posting = []
    page = None
    
    req = requests.get(settings.BASE_URL.format(post_id))
    
    if req.status_code == requests.codes.ok:
        page = BeautifulSoup(req.text, 'html.parser')
    else:
        raise ValueError("Page could not be accessed: " + settings.BASE_URL.format(post_id))
    
    posts = page.find_all("tr", class_ = "athing")
    
    
    for p in posts:
       if p.find("img", width="0"):
           jobs_posting.append(p)
    
    total_posts = len(jobs_posting) 
    
    for item in jobs_posting:
        for kw in keywords:
            if kw.lower() in item.text.lower():
                kw_counter[kw] +=1
        if combinations:
            #print(combinations)
            for c in combinations:
                if all([comb in item.text.lower() for comb in c.lower().split('-')]):
                    comb_counter[c] +=1
    
    print ('Total job posts: {}'.format(len(posts)-1))
    print ('Keywords:')
    for k in keywords:
        pct = int(float(kw_counter[k])/len(posts)*100)
        print('{}: {} ({}%)'.format(k.title(), kw_counter[k], pct))
    
    if combinations:
        print('Combinations:')
        for c in combinations:
            pct = int(float(comb_counter[c])/len(posts)*100)
            print('{}: {} ({}%)'.format(c.title(), comb_counter[c], pct))
    


if __name__ == '__main__':
    jobs_detector()
    
