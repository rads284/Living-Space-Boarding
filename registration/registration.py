from pymongo import MongoClient
from flask import Flask, request, jsonify

app = Flask(__name__)
conn = sqlite3.connect('livingspace.db', check_same_thread=False)
c = conn.cursor()

@app.route('/register',methods=['POST'])
def hello():
	try:
		if(request["user-type"]=="warden"):
			c.execute("INSERT INTO Warden (FullName,Id,PhoneNumber,Password,Email) VALUES (?, ?, ?, ?, ?);",request.json["full-name"],request.json["id"],request.json["phone-number"],request.json["password"],request.json["email"])
		elif(request["user-type"]=="parent"):
			c.execute("INSERT INTO Parent (FullName,Id,PhoneNumber,Password,Email,) VALUES (?, ?, ?, ?, ?);",request.json["full-name"],request.json["id"],request.json["phone-number"],request.json["password"],request.json["email"])
		elif(request["user-type"]=="student"):
			c.execute("INSERT INTO Student (w_id,Id,FullName,p_id) VALUES (?, ?, ?, ?);",request.json["w_id"],request.json["id"],request.json["full-name"],request.json["p_id"])

		conn.commit()
		conn.close()
		return jsonify("Added to Database Successfully!"),200
	except:
		return jsonify("Database Error!"),400

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8080,debug=True)
