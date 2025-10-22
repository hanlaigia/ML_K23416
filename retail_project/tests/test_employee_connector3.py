from retail_project.connectors.employee_connector import EmployeeConnector
from retail_project.models.employee import Employee

ec = EmployeeConnector()
ec.connect()
emp = Employee()
emp.ID=20
emp.EmployeeCode = "EMP114"
emp.Name = "Doraemun"
emp.Phone = "113"
emp.Email = "doraemon@yahoo.com"
emp.Password = "456"
emp.IsDelete = 0

result = ec.update_one_employee(emp)
if result > 0:
    print("Chuc mung nha, sua thanh cong")
else:
    print("That dang thuong")


# from retail_project.connectors.employee_connector import EmployeeConnector
# from retail_project.models.employee import Employee
#
# ec = EmployeeConnector()
# ec.connect()
# emp = Employee()
# emp.ID = 7
# emp.EmployeeCode = "EMP414"
# emp.Name = "K23414"
# emp.Phone = "03423523432"
# emp.Email = "k23416@gmail.com"
# emp.Password = "123"
# emp.IsDeleted = 0
#
# result = ec.update_one_employee(emp)
# if result> 0:
#     print("update ngon")
# else:
#     print("udate failed")
