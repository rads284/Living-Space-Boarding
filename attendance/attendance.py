from flask import Flask, request
from flask_cors import CORS, cross_origin
import sqlite3
import os

app = Flask(__name__)
CORS(app, support_credentials=True)

con = sqlite3.connect('livingspace.db', check_same_thread=False)
con.execute("PRAGMA foreign_keys = ON")

@app.route('/markattendance', methods=['GET', 'POST'])
def markattendance():
	if(request.method == 'GET'):
		c = con.cursor()
		students =c.execute("SELECT Id,FullName FROM Student")
		l=students.fetchall()
		retstr = ""
		count = 0
		for i in l:
			retstr += "("
			retstr += i[0]
			retstr += ","
			retstr += i[1]
			retstr += ")"
			retstr += "!"
			count +=1
			if count == 5:
				break
		return retstr,200
	elif(request.method == 'POST'):
		from datetime import datetime
		req = request.json
		for key in req.keys():
			if req[key]["present"]==False:
				c = con.cursor()
				now = datetime.now()
				now_date = now.strftime("%d-%m-%Y")
				c.execute("INSERT INTO Attendance (CDate, s_id) VALUES (?,?);",(now_date, key))
				con.commit()

		return "",200
	else:
		return '',405


@app.route("/viewattendance", methods=['GET'])
def viewattendance():
	if(request.method == 'GET'):
		app.logger.info(request.args)
		ID=request.args.get('id',type=str)
		c = con.cursor()
		name = c.execute("SELECT FullName FROM Student WHERE Id = (?);", (ID,))
		name = name.fetchall()
		if len(name) == 0:
			return "No such student ID", 200
		name = name[0][0]
		result = c.execute("SELECT * FROM Attendance")
		result = result.fetchall()
		result = c.execute("SELECT * FROM Attendance WHERE s_id = (?);", (ID,))
		result = result.fetchall()
		if len(result) == 0:
			return "This student attended all days", 200
		string = ""
		string += name + "!"
		string += result[0][1] + "!"
		for i in result:
			string += i[0]
			string += "!"
		return string,200
	else:
		return "", 405

if __name__ == '__main__':
	app.run( debug=True,
            host=os.getenv('LISTEN', '127.0.0.1'),
            port=int(os.getenv('PORT', '5000'))
            )