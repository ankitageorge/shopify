from datetime import datetime
from urllib.parse import urlparse

class Image():
	def __init__(self, title, tags, url, index='images'):
		if not title or not tags or not url:
			raise ValueError("All fields are required for this form.")
		if not urlparse(url).scheme:
			raise ValueError("Image url must be valid in the form.")

		self.title = title
		self.tags = tags.split(',')
		self.url = url

	def add_to_db(self, es, index='images'):
		body = {
			'title': self.title,
			'tags': self.tags,
			'url': self.url,
			'timestamp': datetime.now()
		}

		result = es.index(index=index, body=body)
		return result

	@staticmethod
	def get_by_id(es, id, index='images'):
		return es.get(index=index, id=id)

	@staticmethod
	def search(es, keyword, index='images'):
		body = {
			"query": {
				"multi_match": {
					"query": keyword,
					"fields": ["title", "tags"],
					"fuzziness": 5
				}
			}
		}

		res = es.search(index=index, body=body)
		return res['hits']['hits']


	@staticmethod
	def get_images_info_for_display(results):
		images = [[res['_source']['url'], res['_source']['title']] for res in results]
		return images

	@staticmethod
	def load_all_images(es, index='images'):
		body = {
			"query": {
				"match_all": {
				}
			}
		}

		res = es.search(index=index, body=body)
		return res['hits']['hits']



