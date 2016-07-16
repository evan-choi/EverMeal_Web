from app.blueprint import basic
from flask import jsonify

@basic.route('/')
def index():
	return "hello ljs93kr!!"

@basic.route('/data')
def data():
	data = {"names": ["John", "Jacob", "Julie", "Jennifer"]}
	return jsonify(data)