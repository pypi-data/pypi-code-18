from bs4 import BeautifulSoup
from urllib import request


class OddsWatcher(object):
    def __get_request_via_get(self, url):
        source = request.urlopen(url)
        return source

    def __find_hid(self, td):
        # get hid
        for link in td.findAll('a'):
            url = link.attrs['href']
            if "/horse/" in link.attrs['href']:
                tmp = url.split('/')
                return tmp[4]
        return None

    def __find_rid(self, td):
        # get rid
        for link in td.findAll('a'):
            url = link.attrs['href']
            if "&" in url:
                tmp = url.split('&')
                tmp = tmp[1].split('=')
                return tmp[1][1:]
        return None

    def __extract_time(self, text):
        text = text.strip()
        time = text[:5]
        return time

    def __2dict(self, df, time_df):
        if len(df) != len(time_df):
            print("file length is different. void dictionalize")
            return
        dict = {}
        for (rid, time) in zip(df, time_df):
            dict[time] = rid
        return dict

    def __find_race_time(self, div):
        text = div.text
        time = self.__extract_time(text)
        if time is not None:
            return time
        return None

    def __scrape_race_info(self, source):
        soup = BeautifulSoup(source, "lxml")
        df = []
        # Extract status
        title = soup.find('h1')
        print(title.text)
        self.title = title.text
        # if title.text is not correct (e.g. another race), remove
        table = soup.find(class_='race_table_old nk_tb_common')
        for tr in table.findAll('tr', ''):
            row = []
            for td in tr.findAll('td', ''):
                # get house status
                word = " ".join(td.text.rsplit())
                row.append(word)

                hid = self.__find_hid(td)
                if hid is not None:
                    row.append(hid)
            df.append(row)
        return df

    def __scrape_race_id(self, source):
        soup = BeautifulSoup(source, "lxml")
        df = []
        time_df = []
        body = soup.find(id="race_list_body")
        for col in body.findAll(class_='race_top_hold_list'):
            row = []
            times = []
            for div in col.findAll(class_='racename'):
                rid = self.__find_rid(div)
                if rid is not None:
                    row.append(rid)
            df.append(row)

            for div in col.findAll(class_='racedata'):
                time = self.__find_race_time(div)
                if time is not None:
                    times.append(time)
            time_df.append(times)
            dict = self.__2dict(row, times)
            yield dict
        # return df, time_df

    def get_race_odds(self, race_id):
        url = 'http://race.netkeiba.com/?pid=race_old&id=c' + str(race_id)
        source = self.__get_request_via_get(url)
        self.df = self.__scrape_race_info(source)
        odds_list = [x[10] for x in self.df if len(x) > 0]
        return odds_list

    def get_race_ids(self, date):
        # url = 'http://race.netkeiba.com/?pid=race_list&id=c' + str(date)
        url = 'http://race.netkeiba.com/?pid=race_list&id=p' + str(date)
        source = self.__get_request_via_get(url)
        dict = {}
        for d in self.__scrape_race_id(source):
            dict.update(d)
        print(dict)
        # df, time_df = self.__scrape_race_id(source)
        # print(df, time_df)
