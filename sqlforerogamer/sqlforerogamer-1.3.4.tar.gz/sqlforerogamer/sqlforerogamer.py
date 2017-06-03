import pandas as pd
import requests
from bs4 import BeautifulSoup

EROGAME_SCAPE_SQL_URL = 'http://erogamescape.dyndns.org/~ap2/ero/toukei_kaiseki/sql_for_erogamer_form.php'

def read(sql):
    http_responce = requests.post(EROGAME_SCAPE_SQL_URL, {'sql': sql})
    html = http_responce.content
    try:
         df = pd.read_html(html)[0].pipe( lambda df: df.rename(columns=df.iloc[0]) ).drop(0).reset_index()

    except ValueError:
        message = BeautifulSoup(html, "lxml").find(id='query_result_main').get_text()
        raise ValueError(message)
    return df

def tables():
    return read('select schemaname, relname from pg_stat_user_tables')
