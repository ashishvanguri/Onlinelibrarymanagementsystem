from flask import Flask, render_template, request, make_response, session, url_for
import requests
import mysql.connector
from werkzeug.utils import redirect

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345",
    database="library"
)

mycursor = mydb.cursor()

app = Flask(__name__)
app.secret_key = "abc"
admin_login = 0
stud_login = 0


@app.route('/')
def main():
    return render_template('home.html')


@app.route('/studlogin', methods=['POST', 'GET'])
def home():
    data = ""
    return render_template('studentlogin.html', data=data)


from MySQLTest import login_student


@app.route('/studloginpage', methods=['POST', 'GET'])
def student_page():
    uname = request.form['uname']
    pwd = request.form['pwd']
    result = login_student(uname, pwd)
    if result != "Not Found":
        res = make_response(render_template('studenthome.html', data="Welcome " + str(result[3])))
        session['result'] = result
        print(session['result'])
        return res
    else:
        return render_template('studentlogin.html', data='Username Or Password is Wrong Please login again')
@app.route('/studentsignup')
def stud_sign_up():
    return render_template('studentsignup.html')
@app.route('/studentregister',methods=['POST','GET'])
def stud_sign():
    try:
        uname = str(request.form['studuname'])
        name = str(request.form['studname'])
        pwd = str(request.form['studid'])
        id = str(request.form['studpw'])
        print(
            "insert into students(id,username,password,name) values(" + id + ',"' + uname + '","' + pwd + '","' + name + '");')
        mycursor.execute(
            "insert into students(id,username,password,name) values(" + id + ',"' + uname + '","' + pwd + '","' + name + '");')

        mydb.commit()
        return render_template("studentlogin.html",data='Student Added Successfully!')
    except Exception as e :
        return render_template('studentlogin.html',data=e)

@app.route('/studhome')
def stud_home():
    if len(session) > 0:
        print(len(session))
        return render_template("studenthome2.html")
    else:
        return render_template('studentlogin.html', data="Please Login First")


@app.route('/logout')
def logout():
    session.pop('result', None)
    admin_login=0
    return redirect(url_for('main'))


@app.route('/viewprofile')
def view_profile():
    if len(session) > 0:
        res = session['result']
        return render_template("viewprofile.html", id=str(res[0]), name=str(res[3]), username=str(res[1]))
    else:
        return redirect("/")


@app.route('/viewprofilefaculty')
def view_profile_faculty():
    if len(session) > 0:
        res = session['result']
        return render_template("viewprofilefaculty.html", id=str(res[0]), name=str(res[3]), username=str(res[1]))
    else:
        return redirect("/")


@app.route('/changepasswordfaculty')
def change_password_faculty():
    if len(session) > 0:
        return render_template("changepasswordfaculty.html")
    else:
        return render_template("facultyloginpage.html", data="Please Login first")


@app.route('/changepassword')
def change_password_stud():
    if len(session) > 0:
        return render_template("changepassword.html")
    else:
        return render_template("studentlogin.html")


from MySQLTest import change_password_faculty3


@app.route('/passwordchangedfaculty', methods=['POST', 'GET'])
def change_password_faculty2():
    pw = request.form['passoword3']
    pw2 = request.form['password4']
    usname = session['result'][2]
    change_password_faculty3(usname, pw2)
    return render_template("facultyhomepage.html", message="Password Changed Successfully")


@app.route("/lendedbooksfaculty")
def books_lended_faculty():
    res = session['result']
    print(res[0])
    mycursor.execute("select * from lendedbooks2 where lender_id = '" + str(res[0]) + "';")
    result = mycursor.fetchall()
    return render_template("bookslendedfaculty.html", message=result)


from MySQLTest import change_password


@app.route('/passwordchanged', methods=['POST', 'GET'])
def change_stud():
    usname = session['result'][1]
    pw = request.form['passoword1']
    pw2 = request.form['password2']
    change_password(usname, pw2)
    return render_template("studenthome2.html", message="Password Changed Successfully")


@app.route("/lendedbooks")
def lended_disp_stud():
    res = session['result']
    mycursor.execute("select * from lendedbooks2 where lender_id = '" + str(res[0]) + "';")
    result = mycursor.fetchall()
    return render_template("lendedbooks.html", message=result)


@app.route("/facultylogin")
def faculty_login_page():
    return render_template("facultyloginpage.html")


@app.route('/search')
def search():
    mycursor.execute("select * from books where availability = 'y' or availability = 'Y';")
    result = mycursor.fetchall()
    return render_template('search.html', message=result)


from MySQLTest import login_faculty


@app.route("/facultyloginpage", methods=['POST', 'GET'])
def faculty_login():
    uname = request.form['uname']
    pwd = request.form['pwd']
    result = login_faculty(uname, pwd)
    if result != "Not Found":
        res = make_response(render_template('facultyhome.html', data="Welcome " + str(result[1])))
        session['result'] = result
        return res
    else:
        return render_template('facultyloginpage.html', data='Username Or Password is Wrong Please login again')


@app.route('/viewbooksfaculty')
def view_books_faculty():
    mycursor.execute("select * from books where availability = 'y' or availability = 'Y';")
    result = mycursor.fetchall()
    return render_template("viewbooksfaculty.html", message=result)


@app.route('/facultyhome', methods=['GET', 'POST'])
def faculty_next():
    return render_template("facultyhomepage.html")


# admin
@app.route('/adminlogin')
def admin_login():
    return render_template("adminlogin.html")


from MySQLTest import *


@app.route('/adminhomepage', methods=['POST', 'GET'])
def admin_login_():
    uname = request.form['aduname']
    pwd = request.form['adpwd']
    result = login_admin(uname, pwd)
    if result != "Not Found":
        global admin_login
        admin_login = 1
        res = make_response(render_template('adminhome.html', data="Welcome " + str(result[1])))
        session['result'] = result
        return res
    else:
        return render_template('adminloginpage.html', data='Username Or Password is Wrong Please login again')
    return render_template()


@app.route('/viewallstudents')
def admin_view_all_students():
    mycursor.execute("select * from students")
    result = mycursor.fetchall()
    return render_template('adminviewallstudents.html', message=result)


@app.route('/addstudent')
def add_student():
    global admin_login
    if admin_login == 1:
        return render_template('adminaddstudent.html')
    else:
        return render_template("adminlogin.html")


@app.route('/addstudentsuccess',methods=['POST','GET'])
def add_student_db():
    try:
        uname = str(request.form['studuname'])
        name = str(request.form['studname'])
        pwd = str(request.form['studid'])
        id = str(request.form['studpw'])
        print(
            "insert into students(id,username,password,name) values(" + id + ',"' + uname + '","' + pwd + '","' + name + '");')
        mycursor.execute(
            "insert into students(id,username,password,name) values(" + id + ',"' + uname + '","' + pwd + '","' + name + '");')

        mydb.commit()
        return render_template("adminhome.html",message='Student Added Successfully!')
    except Exception :
        return render_template('adminhome.html',message='Username Already exists!!')

@app.route('/deletestudent')
def delete_student():
    global admin_login
    if(admin_login==1):
        mycursor.execute("select * from students;")
        result = mycursor.fetchall()
        return render_template("deletestudent.html",message=result)
    else:
        return render_template("adminlogin.html")
@app.route('/studentdeleted',methods=['POST','GET'])
def deleted_student():
    delte = request.form.get('deletestud')
    mycursor.execute("delete from students where username = '"+delte+"';")
    mydb.commit()
    return render_template('adminhome.html',message=str(delte) + " is deleted")
#adminbooks
@app.route('/adminviewallbooks')
def view_books():
    global admin_login
    mycursor.execute("select * from books;")
    result = mycursor.fetchall()
    if(admin_login==1):
        return render_template('adminviewallbooks.html',message=result)
    else:
        return render_template("adminlogin.html")
@app.route('/adminaddbook')
def add_book():
    global admin_login
    if(admin_login==1):
        return render_template('adminaddbook.html')
    else:
        return render_template("adminlogin.html")
@app.route('/adminbookadded',methods=['POST','GET'])
def add_book_to_db():
    bname = str(request.form['bookname'])
    author = str(request.form['author'])
    bookid = str(request.form['bookid'])
    isbn = str(request.form['isbn'])
    mycursor.execute(
        "insert into books(book_id,bookname,author,ISBN,availability) values(" + bookid + ',"' + bname + '","' + author + '","' + isbn + '","Y");')
    mydb.commit()
    return render_template("adminhome.html",message='Added Book')
@app.route('/admindeletebook')
def admin_del_book():
    mycursor.execute("select * from books;")
    result = mycursor.fetchall()
    return render_template('admindeletebook.html',message=result)
@app.route('/adminbookdeleted',methods=['POST','GET'])
def del_book_db():
    res = request.form.get('deletebook')
    mycursor.execute("delete from books where book_id = " + str(res)+";" )
    mydb.commit()
    return render_template('adminhome.html',message="Deleted Successfully!!")
@app.route('/adminissuebook')
def issue_book():
    mycursor.execute("select * from books where availability = 'Y';")
    result = mycursor.fetchall()
    mycursor.execute('select * from students')
    result2 = mycursor.fetchall()
    mycursor.execute('select *  from faculty;')
    result3 = mycursor.fetchall()
    return render_template('adminissuebook.html',message=result,message2=result2,message3=result3)
@app.route('/bookissuedsuccess',methods=['POST','GET'])
def bookissuedb():
    book = request.form.get('bookissue')
    mycursor.execute("select bookname from books where book_id ="+str(book)+";")
    result = mycursor.fetchall()
    bookname = result[0][0]
    student = request.form.get('studentissue')
    if student[0]=='F':
        mycursor.execute("insert into lendedbooks2(book_id,bookname,lender_id) values("+str(book)+",'"+bookname+"',"+student[1:]+");")
        mydb.commit()
    return render_template('adminhome.html',message="Issued Book " + bookname +" Successfully")
@app.route('/adminbookreturn')
def book_return_page():
    mycursor.execute("select * from lendedbooks2;")
    result = mycursor.fetchall()
    return render_template("adminbookreturn.html",message=result)
@app.route('/returnedsuccessfully',methods=['POST','GET'])
def returned_success():
    book = str(request.form.get('returnbook'))
    print(book)
    mycursor.execute("delete from lendedbooks2 where book_id="+book+";")
    mydb.commit()
    return render_template('adminhome.html', message="Returned Sucessfully")
#faculty-admin
@app.route('/adminviewfaculty')
def admin_view_all_faculty():
    mycursor.execute("select * from faculty;")
    result = mycursor.fetchall()
    return render_template('adminallfaculty.html', message=result)
@app.route('/adminaddfaculty')
def add_faculty():
    global admin_login
    if admin_login == 1:
        return render_template('adminaddfaculty.html')
    else:
        return render_template("adminlogin.html")
@app.route('/addfacultysuccess',methods=['POST','GET'])
def add_faculty_db():
    try:
        uname = str(request.form['facuname'])
        name = str(request.form['facname'])
        pwd = str(request.form['facpw'])
        id = str(request.form['facid'])
        print(
            "insert into faculty(id,name,username,password) values(" + id + ',"' + name + '","' + uname + '","' + pwd + '");')
        mycursor.execute(
            "insert into faculty(id,name,username,password) values(" + id + ',"' + name + '","' + uname + '","' + pwd + '");')

        mydb.commit()
        return render_template("adminhome.html",message='Faculty Added Successfully!')
    except Exception  as e:
        print(e)
        return render_template('adminhome.html',message='Username Already exists!!')
@app.route('/admindeletefaculty')
def delete_faculty():
    global admin_login
    if(admin_login==1):
        mycursor.execute("select * from faculty;")
        result = mycursor.fetchall()
        return render_template("admindeletefaculty.html",message=result)
    else:
        return render_template("adminlogin.html")
@app.route('/facultydeleted',methods=['POST','GET'])
def deleted_faculty():
    delte = request.form.get('deletefaculty')
    mycursor.execute("delete from faculty where username = '"+delte+"';")
    mydb.commit()
    return render_template('adminhome.html',message=str(delte) + " is deleted")


if __name__ == "__main__":
    app.run(debug=True)
