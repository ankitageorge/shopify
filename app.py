from flask import Flask, render_template, jsonify, request
from elasticsearch import Elasticsearch
from datetime import datetime
import json
from urllib.parse import urlparse


# DEVELOPMENT_ENV  = True

app = Flask(__name__)
es = Elasticsearch()


@app.route('/', methods=['GET'])
def index():
	# results = es.get(index="images", id="1")
	body = {
		"query": {
			"match_all": {
			}
		}
	}

	res = es.search(index="images", body=body)
	images = get_images_info(res['hits']['hits'])

	return render_template('index.html', images=images)
    # return jsonify(results['_source'])


@app.route('/new_image', methods=['GET','POST'])
def new_image():
	if request.method == 'POST':
		title = request.form['title']
		tags = request.form['tags']
		url = request.form['url']

		if not title or not tags or not url:
			message = "All fields are required for this form."
			return render_template("error.html", message=message)
		if not urlparse(url).scheme:
			message = "Image url must be valid in the form."
			return render_template("error.html", message=message)

		body = {
			'title': title,
			'tags': tags.split(','),
			'url': url,
			'timestamp': datetime.now()
		}

		result = es.index(index='images', body=body)

		return render_template("success.html")
	else:
		return render_template("form.html")


@app.route('/get_image/<image_id>', methods=['GET'])
def get_image(image_id):
	# id = request.view_args['image_id']
	
	result = es.get(index='images', id=image_id)
	# vaPpgHIB6EquDrw2FnjL
	return jsonify(result)


@app.route('/search', methods=['GET', 'POST'])
def search():
	if request.method == 'POST':
		keyword = request.form['keyword']

		body = {
			"query": {
				"multi_match": {
					"query": keyword,
					"fields": ["title", "tags"],
					"fuzziness": 5
				}
			}
		}

		res = es.search(index="images", body=body)

		return display_images(res['hits']['hits'])
	else:
		return render_template('search.html')


def get_images_info(results):
	images = [[res['_source']['url'], res['_source']['title']] for res in results]
	return images

def display_images(results):
	images = get_images_info(results)

	return render_template("gallery.html", images=images)

if __name__ == '__main__':
	app.run()