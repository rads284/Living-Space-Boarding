from flask import Flask, jsonify, abort, request, redirect
from flask import url_for, json, make_response, render_template
from flask_mail import Mail, Message
import smtplib
from datetime import datetime
from flask_cors import CORS, cross_origin
import sqlite3
import os
import time
import requests
import logging
import uuid
import random
from werkzeug.exceptions import BadRequest
'''
    Leave management - [create leave request, approve leave request]
    Leave request can be initiated by either warden or parent
    1.
    warden creates leave request- form (date, reason) - backend - notify parent (email)
    parent approves leave - otp verification (use Pkk's service) - db update
    2.
    parent creates leave request - notifies warden(email/sms) - approves - db update
'''

app = Flask(__name__)

CORS(app, support_credentials=True)
conn = sqlite3.connect('../database/livingspace.db', check_same_thread=False)
# conn.execute("PRAGMA foreign_keys = ON")
c = conn.cursor()
'''
Debug True for dev,465 for SSL and set mail server for no spam
'''
app.config.update(
                  DEBUG=True,
                  MAIL_SERVER='smtp.gmail.com',
                  MAIL_PORT=465,
                  MAIL_USE_SSL=True,
                  MAIL_USERNAME='livingspaceboarding@gmail.com',
                  MAIL_PASSWORD='Bandar-vihar'
                 )
mail = Mail(app)


def create_leave(from_t, to_t, reason, sid, w_app="No", p_app="No"):
    from_t = '-'.join(from_t.split('-')[::-1])
    to_t = '-'.join(to_t.split('-')[::-1])
    leave_id = str(uuid.uuid1())
    row = (leave_id, sid, from_t, to_t, w_app, p_app)
    c.execute("INSERT INTO Leave(id,s_id,CheckIn,CheckOut,ApprovedW,ApprovedP) VALUES(?,?,?,?,?,?)", row)
    return leave_id


OTP = 0000


@app.route('/verify_otp',methods=['POST'])
def verify_otp():
    otp = request.form.get("otp")
    leaveid = request.form["leaveid"]
    global OTP
    if(OTP == int(otp)):
        return "Success", 200
    else:
        return "Failure", 400


@app.route('/notify_parent', methods=['POST'])
def notify_parent():
    logging.info(request.form)
    print(request.form)
    try:
        from_t = request.form.get("from", False)
        to_t = request.form["to"]
        reason = request.form["reason"]
        sid = request.form["sid"]
    except Exception as e:
        return BadRequest("The data provided is invalid")
    leave_id = create_leave(from_t, to_t, reason, sid, "Yes")
    global OTP
    OTP = random.randint(1000,9999)

    c.execute("SELECT Email from Parent where Id = ( SELECT p_id from Student where Id = '%s')" % sid)
    parent_id = c.fetchone()[0]
    c.execute("SELECT FullName from Student where Id ='%s'" % sid)
    student_name = c.fetchone()[0]
    leave_url = "https://LivingSpaceBoarding/LeaveApprove/?leave_id=" + leave_id
    msg = Message('Leave Request Approval', sender='livingspaceboarding@gmail.com', recipients=[parent_id])
    msg.body = "Dear Parent,\n\t Your ward, " + student_name + " (Student ID: " + sid + ") has raised a leave application from " + from_t + " to " + to_t + " for the following reason: " + reason + ". Kindly click on the following link to approve the Leave Request : " + leave_url +  "\nYOUR OTP IS : "+ str(OTP) + "\n\n Regards,\nLivingSpaceBoarding" 
    try:
        mail.send(msg)
    except Exception as e:
        return 500
    return "Message Sent!"


@app.route('/notify_warden', methods=['POST'])
def notify_warden():
    try:
        from_t = request.form.get("from", False)
        to_t = request.form["to"]
        reason = request.form["reason"]
        sid = request.form["sid"]
    except Exception as e:
        return BadRequest("The data provided is invalid")
    c.execute("SELECT Email from Warden where Id = (SELECT w_id from Student where Id = '%s')" % sid)
    warden_id = c.fetchone()[0]
    logging.info("Warden mail Id:", warden_id)
    c.execute("SELECT FullName from Student where Id ='%s'" % sid)
    student_name = c.fetchone()[0]
    # insert into Leave
    OTP = random.randint(1000,9999)
    leave_id = create_leave(from_t, to_t, reason, sid, p_app="Yes")
    leave_url = "https://LivingSpaceBoarding/LeaveApprove/?leave_id=" + leave_id
    msg = Message('Leave Request Approval', sender='livingspaceboarding@gmail.com', recipients=[warden_id])
    msg.body = "Dear Warden,\n\t Parent of " + student_name + " (Student ID: " + sid+")  has raised a leave application from " + from_t + " to " + to_t + " for the following reason: " + reason + ". Kindly click on the following link to approve the Leave Request : " + leave_url + "\nYOUR OTP IS : "+ str(OTP)
    try:
        mail.send(msg)
    except Exception as e:
        return 500
    return "Message Sent!"


@app.route('/approve_leave', methods=['PUT'])
def approve_leave():
    logging.info(request.form)
    leave_id = request.args['leave_id']
    c.execute("SELECT ApprovedP,ApprovedW from Leave where Id='%s'" % leave_id)
    a_p, a_w = c.fetchone()
    if(a_p):
        c.execute("UPDATE  Leave SET ApprovedW='Yes' where Id ='%s'" % leave_id)
    else:
        c.execute("UPDATE  Leave SET ApprovedP='Yes' where Id ='%s'" % leave_id)
    return "Leave Approved!"


@app.route('/get_s_names/<id>/<utype>', methods=['GET'])
def get_s_names(id, utype):
    if(utype == 'warden'):
        c.execute("SELECT FullName from Student where w_id = '%s'" % id)
    else:
        c.execute("SELECT FullName from Student where p_id = '%s'" % id)
    s_names = c.fetchall()
    return json.dumps(s_names)

@app.route('/get_leaves/<id>/<utype>', methods=['GET'])
def get_leaves(id, utype):
    if(utype == 'warden'):
        c.execute("SELECT * from leave where s_id = (SELECT s_id from Warden where w_id = '%s')" % id)
    else:
        c.execute("SELECT * from leave where s_id = (SELECT s_id from Parent where p_id = '%s')" % id)
    leave_details = c.fetchall()
    return json.dumps(leave_details)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)

'''
For testing: Student id 99- parent:preet, warden: rasya
'Parent2-pragnyasuresh@gmail.com,Parent99-preethercules@gmail.com','Parent0prajwalkirankumar@gmail.com','Parent1prajwal.m.nadagouda@gmail.com',
'Warden0rasya.ramesh1999@gmail.com','Warden1rahul.shivaprasad@gmail.com','Warden2ramyani.ghosh@gmail.com','Warden3-agarwal.radhika098@gmail.com'
'''
