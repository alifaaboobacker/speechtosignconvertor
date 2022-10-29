from flask import *

from src.dbconnection import *

app = Flask(__name__)

@app.route('/login',methods=['post'])
def login():
    uname = request.form['uname']
    pwd = request.form['pswd']
    qry = "Select * from Login where Username=%s and Password=%s and type='user'"
    val = (uname,pwd)
    res = selectone(qry,val)
    if res is None:
        return jsonify({'task':'invalid'})

    else:
        id=res[0]
        return jsonify({'task':'valid',"id":id})

@app.route('/registration',methods=['post'])
def registration():
    fname = request.form['fname']
    lname = request.form['lname']
    email = request.form['email']
    phone = request.form['phone']
    username=request.form['uname']
    password=request.form['pswd']
    qry = "insert into login values(NULL,%s,%s,'user')"
    val=(username,password)
    id=iud(qry,val)
    qry1 = "insert into registration values(NULL,%s,%s,%s,%s,%s)"
    val1 = (fname,lname,email,phone,str(id))
    iud(qry1,val1)
    return jsonify({'task':'valid'})
@app.route('/viewnotification',methods=['post'])
def viewnotification():
    qry="select * from notification"
    res=androidselectallnew(qry)
    return jsonify(res)
@app.route('/feedback', methods=['post'])
def feedback():
    feedbackmsg = request.form['msg']
    userid = request.form['uid']
    qry = "insert into feedback values(NULL,%s,curdate(),%s)"
    val = (feedbackmsg,userid)
    iud(qry,val)
    return jsonify({'task':'valid'})
@app.route('/viewtips',methods=['post'])
def viewtips():
    qry ="select * from tips"
    res = androidselectallnew(qry)
    return jsonify(res)



app.run(port=5000,host='0.0.0.0')