from flask import Flask,url_for, render_template, redirect,request,session
import hashlib
import mysql.connector as mysc

app=Flask(__name__)
app.secret_key='fagqt4aevzvnfg'


db = mysc.connect(host='127.0.0.1',user='nayemuddin',password='NayemUddin2000',database='users')
mycursor = db.cursor()

@app.route('/')
def login():
  return render_template('index.html',message='')



@app.route('/signup')
def signup():
  return render_template('sign-up.html')


@app.route('/signup',methods=['POST'])
def registered():
  if request.method=='POST':
    name = request.form['name']
    dob = request.form['date-of-birth']
    gender = request.form['gender']
    phone = request.form['phone'] + str(request.form['number'])
    address = request.form['address']
    email = request.form['email']
    useraname = request.form['username']
    password=pass_encrypt(request.form['password'])
    mycursor.execute('select email,username from user_info where email= %s or username=%s',(email,useraname,))
    res = mycursor.fetchone()
    if not res:
      mycursor.execute(
        'insert into user_info(fullname,date_of_birth,gender,phone,address,username,email,pass) values (%s,%s,%s,%s,%s,%s,%s,%s)',(name,dob,gender,phone,address,useraname,email,password,)
        )
      db.commit()
      return redirect(url_for('login'))
    return render_template('sign-up.html',msg='Account already exists')
  


@app.route('/',methods=['POST'])
def logged_in():
  if request.method=="POST":
    email=request.form['email']
    password=pass_encrypt(request.form['password'])
    mycursor.execute('select * from user_info where email=%s',(email,))
    res = mycursor.fetchone()
    if not res:
      return render_template('index.html',msg="Account doesn't exist")
    elif res[-1]!=password:
      return render_template('index.html',msg="Incorrect password")
    head=['ID','Name','Date of Birth','Gender','Contact No.','Present Address','Email ID','Username']
    keys=['id','name','dob','gender','phone','address','email','username']
    elements=len(keys)
    session['id'],session['name'],session['dob'],session['gender'],session['phone'],session['address'],session['email'],session['username'],session['password']=res
    return render_template('dashboard.html',sess=session,header=head,key=keys,e=elements)




@app.route('/')
def logout():
  for key in session.keys():
      session.pop(key,None)
  return redirect(url_for('login'))





def pass_encrypt(password):
  password+=app.secret_key
  password=hashlib.sha1(password.encode())
  return password.hexdigest()