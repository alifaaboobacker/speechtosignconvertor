import functools

from flask import *

from src.dbconnection import *

app = Flask(__name__)
app.secret_key='aaa'


def login_required(func):
    @functools.wraps(func)
    def secure_function():
        if "lid" not in session:
            return redirect("/")
        return func()
    return secure_function




@app.route('/logout')
def logout():
    session.clear()
    return render_template("login.html")

@app.route('/')
def start():
    return render_template('Login.html')
@app.route('/login',methods=['post'])
def login():
    uname = request.form['textfield']
    pwd = request.form['textfield2']
    qry = "Select * from Login where Username=%s and Password=%s"
    val = (uname,pwd)
    res = selectone(qry,val)
    if res is None:
        return '''<script> alert("invalid"); window.location="/"</script>'''
    elif res[3] == "admin":
        session['lid']=res[0]
        return redirect('/adminhome')
    else:
        return '''<script> alert("invalid"); window.location="/"</script>'''
@app.route('/addtips',methods=['get','post'])
@login_required

def addtips():
    return render_template('Addtips.html')
@app.route('/adminhome')
def adminhome():
    return render_template('Adminhome.html')
@app.route('/Managetips',methods=['post','get'])
@login_required
def Managetips():
    qry="select * from tips"
    res = selectall(qry)
    return render_template('Managetips.html',v2=res)
@app.route("/tip",methods=['post'])
@login_required
def tip():
    tmsg = request.form['textarea']
    qry = "insert into tips values(null,%s,curdate())"
    val =(tmsg)
    iud(qry,val)
    return '''<script>alert("success");window.location="/adminhome"</script>'''
@app.route('/delete')
@login_required
def delete():
    id = request.args.get('id')
    qry="delete from tips where id=%s"
    iud(qry,id)
    return '''<script>alert("success");window.location="/Managetips"</script>'''
@app.route('/sendNotification')
@login_required
def sendNotification():

    return render_template('sendNotification.html')
@app.route("/send",methods=['post'])
@login_required
def send():
    ctnt = request.form['textfield']
    ntc = request.form['textarea']
    qry = "insert into notification values(null,%s,%s,curdate())"
    val = (ctnt, ntc)
    iud(qry, val)
    return '''<script>alert("success");window.location="/adminhome"</script>'''


@app.route('/viewfeedbacks')
@login_required
def viewfeedbacks():
    qry="SELECT registration.fname,registration.lname,feedback.* FROM registration JOIN feedback ON registration.loginid=feedback.userid"
    res=selectall(qry)
    return render_template('viewfeedbacks.html',v1=res)
@app.route('/viewusers')
@login_required
def viewusers():
    qry="select * from registration"
    res=selectall(qry)
    return render_template('viewusers.html',v=res)

app.run(debug=True)