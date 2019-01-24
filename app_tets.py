from flask import render_template, flash, redirect, url_for, session, request, logging
from EmployeeModel import *
from UserModel import User
from passlib.hash import sha256_crypt
import json
import jwt,datetime
from wtforms import Form, StringField, TextAreaField, PasswordField, validators

from functools import wraps
from setting import *
print(__name__)
app.config['SECRET_KEY']='anusoni'

# Home
@app.route('/')
def home():
    return render_template('home.html')

# Employees
@app.route('/employees')
def employees():
    return render_template('employees.html', employees=Employee.get_all_employees())


#Single Employee
@app.route('/employee/<string:emp_id>/')
def employee(emp_id):
    return render_template('employee.html', employee=Employee.get_employee(emp_id))

# Register Form Class
class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

# User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = form.password.data
        User.createUser(name,email,username,password)
        flash('You are now registered and can log in','success')
        return redirect('\login')
    return render_template('register.html', form=form)

# User login
@app.route('/login', methods=['GET', 'POST'])
def get_token():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password= request.form['password']
        match=User.username_password_match(username,password)
        if match:
            # Passed
            session['logged_in'] = True
            session['username'] = username
            flash('You are now logged in','success')
            expiration_date=datetime.datetime.utcnow()+datetime.timedelta(seconds=900)
            token= jwt.encode({'exp':expiration_date},app.config['SECRET_KEY'],algorithm='HS256')
            return redirect('\dashboard')
        else:
            error = 'Invalid login'
            return render_template('login.html', error=error)
    return render_template('login.html')


def token_required(f):
    @wraps(f)
    def wrapper(*args,**kwargs):
        token= request.args.get('token')
        try:
            jwt.decode(token,app.config['SECRET_KEY'])
            return f(*args,**kwargs)
        except:
            return jsonify({'erroe':'Need a valid token'}),401
    return wrapper

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect('\login')
    return wrap

# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect('\login') 

# Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
    return render_template('dashboard.html', employees=Employee.get_all_employees())

# Employee Form Class
class EmployeeForm(Form):
    emp_id = StringField('Employee Id', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    first_name = StringField('First Name', [validators.Length(min=2, max=50)])
    last_name = StringField('Last Name', [validators.Length(min=0, max=50)])
    manager_id = StringField('Manager Name', [validators.Length(min=1 , max=50)])

# Add Employee
@app.route('/add_employee', methods=['GET', 'POST'])
@is_logged_in
def add_employee():
    form = EmployeeForm(request.form)
    if request.method == 'POST' and form.validate():
        emp_id = form.emp_id.data
        username = form.username.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        manager_id = form.manager_id.data
        Employee.add_employee(emp_id,username,first_name,last_name,manager_id)
        flash('Employee Entry is succesfully done', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_employee.html', form=form)

    
    
 
		


app.run(port=5000)
