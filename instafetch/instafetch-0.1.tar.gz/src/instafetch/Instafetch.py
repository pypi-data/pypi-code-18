import requests
import json

q_url = "https://instagram.com/{}/?__a=1"
s_url  = "https://www.instagram.com/web/search/topsearch/?query={}"

class Instafetch: 
	def __init__(self):
		pass

	def users(self, keyword):
		data = requests.get(s_url.format(keyword))
		return data.json()

	def user(self, name):
		data = requests.get(q_url.format(name))
		return data.json()

	def explore(self, hashtag, pages=1):
		self.top_posts = {"data":[]}
		self.posts = {"data":[]}
		explore_url = q_url.format("explore/tags/"+hashtag)

		d = json.loads(requests.get(explore_url).text)

		for p in d['tag']['top_posts']['nodes']: 
				self.top_posts["data"].append(p)

		next_cursor = ""
		page = 0
		while next_cursor!=None and page<pages:
			d = json.loads(requests.get(explore_url).text)
			for p in d['tag']['media']['nodes']:
				self.posts['data'].append(p)
			next_cursor = d['tag']['media']['page_info']['end_cursor']
			explore_url = "https://www.instagram.com/explore/tags/{}/?__a=1&max_id={}".format(hashtag, next_cursor)
			page+=1
