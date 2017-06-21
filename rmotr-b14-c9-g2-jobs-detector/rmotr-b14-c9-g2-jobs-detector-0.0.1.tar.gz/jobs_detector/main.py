import click
import requests
from bs4 import BeautifulSoup

from jobs_detector import settings

DEFAULT_KEYWORDS = [
    # set some default keywords here
    'Remote', 'Postgres', 'Python', 'Javascript', 'React','Pandas'
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
    
    url = settings.BASE_URL.format(post_id)
    r = requests.get(url)
    if r.status_code != requests.codes.ok:
        raise Exception('Bad URL: {}'.format(url))
    
    html_doc = r.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    
    comments = soup.find_all( 'td', class_='ind')  
    l_jobs = []
    
    for icomment in comments:
        if icomment.find('img').get('width') == "0":
            span = icomment.parent.find('span', class_='c00')
            l_jobs.append(span.text)
    rs = "Total job posts: {} \nKeywords:\n".format(len(l_jobs))
    
    # keywords statistics
    kw_stat={}
    for kw in keywords.split(','):
        j_count = 0
        for ijob in l_jobs:
            if kw.lower() in ijob.lower():
                j_count += 1
        kw_stat[kw] = j_count
        rs += "{}: {} ({}%)\n".format(kw.title(),j_count,int((float(j_count)/len(l_jobs))* 100))
       
    #Combination statistics
    if combinations:
        combo_stat = {}
        rs += "Combinations:\n"
        for combo in combinations:
            j_count = 0
            for ijob in l_jobs:
                is_match = True
                for kw in combo.split('-'):
                    if not kw.lower() in ijob.lower():
                        is_match = False
                if is_match:
                    j_count += 1
            combo_stat[combo] = j_count
            rs += "{}: {} ({}%)\n".format(combo.title(), j_count, int(float(j_count)/len(l_jobs)* 100))
            
    print(rs)
    
if __name__ == '__main__':
    jobs_detector()

