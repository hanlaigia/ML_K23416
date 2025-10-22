from retail_project.connectors.employee_connector import EmployeeConnector

ec=EmployeeConnector()
ec.connect()
em=ec.login("putin@hotmail.com", "123")
if em==None:
    print("Login Failed")
else:
    print("Login Succeeded")
    print(em)


#test get_all_employee:
print('List of Employee:')
ds=ec.get_all_employee()
print(ds)
for emp in ds:
    print(emp)

id=3
emp=ec.get_detail_infor(id)
if emp==None:
    print("Khong co nhan vien nao co ma =", id)
else:
    print("Tim thay nhan vien co ma =", id)
    print(emp)