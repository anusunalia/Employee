            expiration_date=datetime.datetime.utcnow()+datetime.timedelta(seconds=900)
            token= jwt.encode({'exp':expiration_date},app.config['SECRET_KEY'],algorithm='HS256')
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

@app.route('/employee')
#@token_required
def get_employee():
    return jsonify({'employee':Employee.get_all_employees()})

def validEmployeeEntry(employeeEntry):
    if("emp_id" in employeeEntry and "username" in employeeEntry and "first_name" in employeeEntry):
        return True
    else:
        return False


@app.route('/employee',methods=['POST'])
def add_employee():
    request_data=request.get_json()
    if (validEmployeeEntry(request_data))  :
        Employee.add_employee(request_data['emp_id'],request_data['username'],request_data['first_name'],request_data['last_name'],request_data['manager_id'])
        response=Response("",201,mimetype='application/json')
        response.headers['Location']="/employees/"+str(new_employee['emp_id'])           
        return response
    else:
        invalidEmployeeEntryErrorMsg={
            "errorMsg":" Invalid object passed in request",
            "helpString":"Please enter data similare to {'emp_id':789789,'username':'abc','first_name':'xyz','last_name':'pqrs','manager_id':989} format"
            }
        response=Response(json.dumps(invalidEmployeeEntryErrorMsg),status=400,mimetype='application/json')         
        return response
@app.route('/employees/<int:emp_id>',methods=['PUT'])
def replace_employee(emp_id):
    request_data=request.get_json()
    Employee.replace_employee(request_data['emp_id'],request_data['username'],request_data['first_name'],request_data['last_name'],request_data['manager_id'])
    response=Response("",status=204)
    return response

@app.route('/employees/<int:emp_id>',methods=['PATCH'])
def update_employee(emp_id):
    request_data=request.get_json()
    if("manager_id" in request_data):
        Employee.update_emp_manager(emp_id,request_data['manager_id'])
    request_data=request.get_json()
    response=Response("",status=205)
    response.headers['Location']="/employees/"+str(emp_id) 
    return response

@app.route('/employees/<int:emp_id>',methods=['DELETE'])
def delete_employee(emp_id):
    if(Employee.delete_employee(emp_id)):
        response=Response("",status=205)
        return response
    invalidEmployeeEntryErrorMsg={
        "errorMsg":" Invalid Emp_id passed in request, that is no object exists with such emp_id",
        }
    response=Response(json.dumps(invalidEmployeeEntryErrorMsg),status=400,mimetype='application/json')         
    response.headers['Location']="/employees/"+str(emp_id) 
    return response
              
@app.route('/employees/<int:emp_id>')
def get_employee_by_emp_id(emp_id):
    return_value=Employee.get_employee(emp_id)
    return jsonify(return_value)

