from pymongo import MongoClient
from flask import Flask, request, jsonify
import sqlite3,json
from flask import Response
from flask_cors import CORS

app = Flask(__name__)
conn = sqlite3.connect('../database/livingspace.db', check_same_thread=False)
c = conn.cursor()
CORS(app)

@app.route('/register',methods=['POST'])
def hello():
	try:
		listofparams = [request.form["fullname"],request.form["phonenumber"],request.form["password"],request.form["email"]]
		print(listofparams)
		# c.execute("INSERT INTO Parent (FullName,PhoneNumber,Password,Email) VALUES (?, ?, ?, ?);",listofparams)
		conn.commit()
		return "Success",200
	except Exception as e:
		print(e)
		return "Database Error!",400

if __name__ == '__main__':
    app.run(host="127.0.0.1",port=8080,debug=True)
