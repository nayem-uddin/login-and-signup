from flask import Flask,url_for, render_template, redirect,request,session
import hashlib
import pymysql

app=Flask(__name__)
app.secret_key='fagqt4aevzvnfg'


timeout = 10
connection = pymysql.connect(
  charset="utf8mb4",
  connect_timeout=timeout,
  cursorclass=pymysql.cursors.DictCursor,
  db="defaultdb",
  host="nayemuddin-mnubpial-project-1.h.aivencloud.com",
  password="AVNS_sftvfHF-LZN1CKvPJT1",
  read_timeout=timeout,
  port=18706,
  user="avnadmin",
  write_timeout=timeout,
)
mycursor = connection.cursor()

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
      connection.commit()
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
    elif res['pass']!=password:
      return render_template('index.html',msg="Incorrect password")
    head=['ID','Name','Date of Birth','Gender','Contact No.','Present Address','Email ID','Username']
    keys=['id','fullname','date_of_birth','gender','phone','address','email','username']
    elements=len(keys)
    for key, value in res.items():
      session[key]=value
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



if __name__=='__main__':
  app.run(debug=True)
