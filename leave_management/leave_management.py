from flask import Flask, jsonify, abort, request,redirect,url_for,json,make_response,render_template
from flask_mail import Mail,Message
import smtplib
from datetime import datetime
from flask_cors import CORS, cross_origin
import sqlite3
import os
import requests

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
conn = sqlite3.connect('livingspace.db', check_same_thread=False)
#conn.execute("PRAGMA foreign_keys = ON")
c = conn.cursor()

app.config.update(
                  DEBUG =True, #if email fails, the exact error message is shown -False for production
                  MAIL_SERVER = 'smtp.gmail.com', #so that it doesn't go to spam
                  MAIL_PORT = 465 , #FOR SSL EMAILS
                  MAIL_USE_SSL = True,
                  MAIL_USERNAME  = 'livingspaceboarding@gmail.com',
                  MAIL_PASSWORD = 'Bandar-vihar'
                 )
mail = Mail(app)


@app.route('/notify_parent',methods =['POST'])
def notify_parent():#mail_id goes here
    print(request.form)
    From = request.form.get("from", False)
    From = '-'.join(From.split('-')[::-1])
    To = request.form["to"]
    To = '-'.join(To.split('-')[::-1])
    Reason = request.form["reason"]
    sid = request.form["sid"]
    
    print(From, To, Reason)
    c.execute("SELECT FullName from Student where Id ='%s'" %sid)
    student_name = c.fetchall()[0][0]
    c.execute("SELECT Email from Parent where s_id ='%s'" %sid)
    parent_id =c.fetchall()[0][0]
    print("Parent mail id:",parent_id)
    #insert into Leave-sid, wid, pid, ApprovedP as yes
    c.execute("SELECT w_id from Student where Id ='%s'" %sid)
    wid = c.fetchall()[0][0]
    row = (sid,wid,sid,From,To,"Yes","No")
    print("row:",row)
    c.execute("INSERT INTO Leave(s_id,w_id,p_id,CheckIn,CheckOut,ApprovedP) VALUES(?,?,?,?,?,?)" ,row)
   
    msg = Message('Leave Request Approval', sender = 'livingspaceboarding@gmail.com', recipients=[parent_id])
    msg.body = "Dear Parent,\n\t Your ward, "+student_name+ " (Student ID: "+sid+") has raised a leave application from "+ From+" to "+To+ " for the following reason: "+Reason+". Kindly click on the following link to approve the Leave Request : https://LivingSpaceBoarding/LeaveApprove/\n\n Regards,\nLivingSpaceBoarding"
    mail.send(msg)
    return "Message Sent!" #render some page here
    
@app.route('/notify_warden',methods =['POST'])
def notify_warden():#mail)id goes here
    #retrieve warden id from db
    print(print(request.form))
    sid = request.form["sid"]
    c.execute("SELECT FullName from Student where Id ='%s'" %sid)
    student_name = c.fetchall()[0][0]
    print(student_name)
    From = request.form.get("from", False)
    From = '-'.join(From.split('-')[::-1])
    To = request.form["to"]
    To = '-'.join(To.split('-')[::-1])
    Reason = request.form["reason"]
    c.execute("SELECT w_id from Student where Id ='%s'" %sid)
    l=c.fetchall()
    wid = l[0][0]
    c.execute("SELECT Email from Warden where Id ='%s'" %wid)
    warden_id = c.fetchall()[0][0]
    print("Warden mail Id:",warden_id)
    #insert into Leave
    row = (sid,wid,sid,From,To,"Yes")
    c.execute("INSERT INTO Leave(s_id,w_id,p_id,CheckIn,CheckOut,ApprovedW) VALUES(?,?,?,?,?,?)" ,row)
    msg = Message('Leave Request Approval', sender = 'livingspaceboarding@gmail.com', recipients=[warden_id])
    msg.body =  "Dear Warden,\n\t Parent of " + student_name + " (Student ID: "+sid+")  has raised a leave application from "+ From+" to "+To+ " for the following reason: "+Reason+". Kindly click on the following link to approve the Leave Request : https://LivingSpaceBoarding/LeaveApprove/"
    mail.send(msg)
    return "Message Sent!" #render some page here
    
@app.route('/approve_leave',methods =['POST'])
def approve_leave(): #has to be directed here for both warden and parent
    #otp?
    #update db-(id,s_id,w_id,p_id,CheckIn,CheckOut,ApprovedP,ApprovedW, PRIMARY KEY(id)
    #if parent approves
    print(request.form)
    if(request.form.get("pid",False) == False):#means warden approved
        print("Warden Approved")
        wid = request.form["wid"]
        c.execute("UPDATE  Leave SET ApprovedW='Yes' where w_id ='%s'" %wid)
    else:
        print("Parent Approved")
        pid = request.form["pid"]
        c.execute("UPDATE  Leave SET ApprovedP='Yes' where p_id ='%s'" %pid)
    return "Leave Approved!"


if __name__ == '__main__':
    app.run(debug = True,host='0.0.0.0',port=80)

'''
For testing: Student id 99- parent:preet, warden: rasya
'Parent2-pragnyasuresh@gmail.com,Parent99-preethercules@gmail.com','Parent0prajwalkirankumar@gmail.com','Parent1prajwal.m.nadagouda@gmail.com',
'Warden0rasya.ramesh1999@gmail.com','Warden1rahul.shivaprasad@gmail.com','Warden2ramyani.ghosh@gmail.com','Warden3-agarwal.radhika098@gmail.com'
'''
