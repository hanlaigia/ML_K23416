from retail_project.connectors.employee_connector import EmployeeConnector
from retail_project.models.employee import Employee

ec=EmployeeConnector()
ec.connect()
emp=Employee()
emp.EmployeeCode="EMP888"
emp.Name="Doraemon"
emp.Phone="113"
emp.Email="doraemon@yahoo.com"
emp.Password="456"
emp.IsDelete=0

result=ec.insert_one_employee(emp)
if result>0:
    print("Chuc mung nha, da them thanh cong")
else:
    print("That dang thuong")

