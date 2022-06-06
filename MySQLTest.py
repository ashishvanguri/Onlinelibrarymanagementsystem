import mysql.connector


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="12345",
  database="library"
)

mycursor = mydb.cursor()
i = 1
def login_student(uname,password):
  mycursor.execute("select * from students where username='"+uname +"' and password = '" + password+"';")
  myresult = mycursor.fetchall()
  if len(myresult)!= 0:
    return myresult[0]
  else:
    return "Not Found"
def login_faculty(uname,password):
  mycursor.execute("select * from faculty where username='"+uname +"' and password = '" + password+"';")
  myresult = mycursor.fetchall()
  if len(myresult)!= 0:
    return myresult[0]
  else:
    return "Not Found"
def login_admin(uname,password):
  mycursor.execute("select * from admin where username='"+uname +"' and password = '" + password+"';")
  myresult = mycursor.fetchall()
  if len(myresult)!= 0:
    return myresult[0]
  else:
    return "Not Found"

def change_password(username,newpassword):
  mycursor.execute("update students set password = '"+newpassword + "'where username = '"+username+"';")
  mydb.commit()
  return 0;
def change_password_faculty3(username,newpassword):
  mycursor.execute("update faculty set password = '"+newpassword + "'where username = '"+username+"';")
  mydb.commit()
  return 0;

