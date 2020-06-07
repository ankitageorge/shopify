from flask import Flask, render_template, jsonify, request
from elasticsearch import Elasticsearch
from datetime import datetime
from urllib.parse import urlparse
from classes.image import Image
import importlib

# DEVELOPMENT_ENV  = True

app = Flask(__name__)
es = Elasticsearch()


@app.route('/', methods=['GET'])
def index():
	all_images = Image.load_all_images(es)
	images = Image.get_images_info_for_display(all_images)

	return render_template('index.html', images=images)


@app.route('/new_image', methods=['GET','POST'])
def new_image():
	if request.method == 'POST':
		title = request.form['title']
		tags = request.form['tags']
		url = request.form['url']

		try:
			img = Image(title, tags, url)
		except Exception as e:
			return render_template("error.html", message=str(e))

		img.add_to_db(es)

		return render_template("success.html")
	else:
		return render_template("form.html")


@app.route('/get_image/<image_id>', methods=['GET'])
def get_image(image_id):
	result = Image.get_by_id(es, image_id)
	
	return jsonify(result)


@app.route('/search', methods=['GET', 'POST'])
def search():
	if request.method == 'POST':
		keyword = request.form['keyword']

		result = Image.search(es, keyword)

		return jsonify(result) # load_images_for_display(result)
	else:
		return render_template('search.html')


def load_images_for_display(results):
	images = Image.get_images_info_for_display(results)

	return render_template("gallery.html", images=images)

if __name__ == '__main__':
	app.run()