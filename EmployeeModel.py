from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from setting import app
from sqlalchemy.orm import aliased
from sqlalchemy.orm import joinedload

db= SQLAlchemy(app)

class Employee(db.Model):
    """
    Create an Employee table
    """
    __tablename__ = 'employees'

    id = db.Column(db.Integer)
    emp_id = db.Column(db.String(60), primary_key=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    manager_id = db.Column(db.String(60), db.ForeignKey('employees.emp_id'),nullable=True)
    #manager = db.relationship("Employee", backref='reports',remote_side=[id])
    employees = db.relationship("Employee",lazy="joined",backref=db.backref('manager',remote_side=[emp_id]))
    #employees = db.relationship("Employee",uselist=False)
    

    
    def json(self):
        return {'id':self.id, 'emp_id':self.emp_id,'username':self.username, 'first_name':self.first_name,'last_name':self.last_name,'manager_id':self.manager_id}

    def __repr__(self):
        return str({
            'emp_id':self.emp_id,
            'username':self.username,
            'first_name':self.first_name,
            'last_name':self.last_name,
            'manager_id':self.manager_id
            })

    
    """
    Create Part
    """

    def add_employee(_emp_id,_username,_first_name,_last_name,_manager_id):
        new_Employee= Employee(emp_id=_emp_id,username=_username, first_name=_first_name,last_name=_last_name,manager_id=_manager_id)
        db.session.add(new_Employee)
        db.session.commit()

        

    """
    Retrieve  Part
    """
        
    def get_all_employees():
        return [Employee.json(employee) for employee in Employee.query.all()]

    def get_employee(_emp_id):
        return [Employee.json(employee) for employee in (Employee.query.filter_by(emp_id=_emp_id)) ]


    

    """
    Delete Part
    """

    def delete_employee(_emp_id):
        is_succesful=Employee.query.filter_by(emp_id=_emp_id).delete()
        db.session.commit()
        return is_succesful



    """
    Update Part
    """
    def update_emp_manager(_emp_id,_manager_id):
        employee_to_update=Employee.query.filter_by(emp_id=_emp_id).first()
        employee_to_update.manager_id=_manager_id
        db.session.commit()


    """
    Retrive managerial Part
    """

    def get_manager(_emp_id):
        manager = aliased(Employee)
        return [Employee.json(employee) for employee in (Employee.query.options(joinedload(Employee.employees)).filter_by(emp_id=_emp_id)) ]

    
