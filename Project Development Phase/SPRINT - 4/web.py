import ibm_db

conn_str = ibm_db.connect("DATABASE=bludb;HOSTNAME=fbd88901-ebdb-4a4f-a32e-9822b9fb237b.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32731;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=xbd11666;PWD=sl50jj06TEZWtPSQ",'','')
# conn = ibm_db.connect(conn_str, '', '')

from flask import *  
app = Flask(__name__) 

app.secret_key = 'a'



@app.route("/",methods=['POST','GET']) 
# @app.route("/") 
# @app.route('/')
def hello():
    return render_template('index.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/job_listing')
def job_listing():
    return render_template('job_listing.html')

@app.route('/job_details')
def job_details():
    return render_template('job_details.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/register',methods = ["GET","POST"])
def register():
    if request.method == "POST" :
        registertype = request.form.get("registertype")
        username = request.form.get("username")
        user_mail = request.form.get("email")
        user_password = request.form.get("password")

        sql = "SELECT * FROM users WHERE user_mail =?"
        stmt = ibm_db.prepare(conn_str, sql)
        ibm_db.bind_param(stmt,1,user_mail)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        if account:
            msg = "Account already exists!"
        else:
            sql = "INSERT INTO USERS VALUES(?,?,?,?)"
            prep_stmt = ibm_db.prepare(conn_str, sql)
            ibm_db.bind_param(prep_stmt, 1, registertype)
            ibm_db.bind_param(prep_stmt, 2, username)
            ibm_db.bind_param(prep_stmt, 3, user_mail)
            ibm_db.bind_param(prep_stmt, 4, user_password)
            ibm_db.execute(prep_stmt)
            msg = 'You have successfully registered !'
    else:
        return render_template('register.html')

    return render_template('login.html')

@app.route('/login')
def login():
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']
        sql = "SELECT * FROM users WHERE user_mail =? AND user_password=?"
        stmt = ibm_db.prepare(conn_str, sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        session['loggedin'] = True
        session['username'] = account['USERNAME']
        session['email'] = account['USER_MAIL']
        return render_template('index.html')
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('username', None)
   session.pop('email', None)
   return redirect('/')

@app.route('/single-blog')
def single_blog():
    return render_template('single-blog.html')

@app.route('/apply')
def apply():
    return render_template('apply.html')

@app.route('/uploader')
def uploader():
    return render_template('uploader.php')

if __name__ == "__main__":
    app.run(debug=True)