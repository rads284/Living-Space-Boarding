from flask import Flask, request, jsonify
import sqlite3,json
from flask import Response
from flask_cors import CORS
import requests
app = Flask(__name__)
conn = sqlite3.connect('../database/livingspace.db', check_same_thread=False)
c = conn.cursor()
CORS(app)

OTP_API_KEY = "93d7aa05-eea7-11e9-b828-0200cd936042"

details = ""
@app.route('/otp',methods=['POST'])
def hello():
    global details
    print(request.json)
    if(request.json["task"]=="sendOTP"):

            url = "https://2factor.in/API/V1/"+OTP_API_KEY+"/SMS/"+request.json["PHONE_NUMBER"]+"/AUTOGEN"
            response = requests.get(url,headers = {"Content-type": "application/x-www-form-urlencoded"})
            print("HERE",response.json())
            
            if(response.json()["Status"]=="Success"):
                details = response.json()["Details"]
                return Response({"Status":"Success"},200)
            else:
                return Response(response.json(),400)

    elif(request.json["task"]=="verifyOTP"):
        url = "https://2factor.in/API/V1/"+OTP_API_KEY+"/SMS/VERIFY/"+details+"/"+request.json["OTP_INPUT"]
        response = requests.get(url,headers = {"Content-type": "application/x-www-form-urlencoded"})
        if(response.json()["Status"]=="Success" and response.json()["Details"]=="OTP Matched"):
            return Response({"Status":"Success"},200)
        else:
            return Response(response.json(),400)
    
if __name__ == '__main__':
    app.run(host="127.0.0.1",port=7000, debug=True)


   