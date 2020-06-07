from elasticsearch import Elasticsearch
import unittest
import time
from classes.image import Image

es = Elasticsearch()
class TestImage(unittest.TestCase):
	img_name = "test"
	img_tags = "tag1,tag2"
	img_url = "https://myimage.com"
	test_id = "123"

	index_name = 'test-index'

	def setUp(self):
		index_body = {
					"mappings": {
						"properties": {
    						'title' : {"type": "text" },
            				'tags': {"type": "text"},
            				'url': {"type": "text"} 
            			}
            		}
            	}

		es.indices.create(index=self.index_name, body=index_body)

		body = {
			'title': "NYC",
			'tags': "city,travel",
			'url': "https://google.com/test.jpg"
		}

		es.index(index=self.index_name, id=self.test_id, body=body)

		body = {
			'title': "sunshine",
			'tags': "happy",
			'url': "https://google.com/test1.jpg"
		}

		es.index(index=self.index_name, body=body)

		body = {
			'title': "happy birthday",
			'tags': "candles,celebration",
			'url': "https://google.com/test2.jpg"
		}

		es.index(index=self.index_name, body=body)


	
	def tearDown(self):
		es.indices.delete(index=self.index_name)


	def test_image_success(self):
		img = Image(self.img_name, self.img_tags, self.img_url)
		assert(img.title == self.img_name and img.tags == self.img_tags.split(',') and img.url == self.img_url)


	def test_image_failure(self):
		img_url = "hihowareyou"
		self.assertRaises(ValueError, Image, "", "", img_url)

		self.assertRaises(ValueError, Image, self.img_name, self.img_tags, img_url)

	
	def test_add_to_db(self):
		img = Image(self.img_name, self.img_tags, self.img_url)
		id = img.add_to_db(es, index=self.index_name)['_id']
		es.get(index=self.index_name, id=id)
		es.delete(index=self.index_name,id=id)

	
	def test_get_by_id(self):
		assert(Image.get_by_id(es, self.test_id, index=self.index_name)['_id'] == self.test_id)

	
	def test_search(self):
		time.sleep(10)
		result = Image.search(es, "NYC", index=self.index_name)
		assert(len(result) == 1)

		result = Image.search(es, "happy", index=self.index_name)
		assert(len(result) == 2)

		result = Image.search(es, "computers", index=self.index_name)
		assert(len(result) == 0)

	
	def test_load_all_images(self):
		time.sleep(10)
		assert(len(Image.load_all_images(es, index=self.index_name)) == 3)


if __name__ == '__main__':
    unittest.main()


