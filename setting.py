from flask import Flask
import os
app= Flask(__name__)
file_path = os.path.abspath(os.getcwd())+"\database.db"
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
#app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///C:\\Users\Admin\Desktop\Employee-master\database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False


  
