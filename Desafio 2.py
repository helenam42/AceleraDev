#!/usr/bin/env python
# coding: utf-8

# In[6]:


class Department:
    def __init__(self, name, code):
        self.name = name
        self.code = code

class Employee():
    def __init__(self, code, name, salary, department):
        self.department = department
        self.code = code
        self.name = name
        self.salary = salary
        self.work_hours = 8

    def get_hours(self):
        return self.work_hours

class Manager(Employee):
    def __init__(self, code, name, salary):
        super().__init__(code, name, salary, Department('managers', 1))

    def calc_bonus(self):
        return self.salary * 0.15
    
    def get_hours(self):
        return self.work_hours

    # atualizaçao de departamento

    def get_department(self):
        return self.department.name

    def set_department(self, ndepartment, ncode):
        self.department = Department(ndepartment, ncode)

class Seller(Employee):
    def __init__(self, code, name, salary):
        super().__init__(code, name, salary, Department('sellers', 2))
        self.__sales = 0

    def get_hours(self):
        return self.work_hours

    def get_sales(self):
        return self.__sales

    def put_sales(self, sales):
        self.__sales += sales

    # atualizaçao de departamento

    def get_department(self):
        return self.department.name

    def set_department(self, ndepartment, ncode):
        self.department = Department(ndepartment, ncode)

    def calc_bonus(self):
        return self.__sales * 0.15

