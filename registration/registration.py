from pymongo import MongoClient
from flask import Flask, request, jsonify

app = Flask(__name__)
MONGO_CLIENT = MongoClient('localhost', 27017)
DATABASE = MONGO_CLIENT.db
USER_DETAILS = DATABASE.details

@app.route('/',methods=['POST'])
def hello():
	try:
		USER_DETAILS.insert_one(request.json)
		return "Added to Database Successfully!",200
	except:
		return "Database Error!",400

if __name__ == '__main__':
    app.run(host="localhost",port=8080,debug=True)