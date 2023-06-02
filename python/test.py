from python.Repository.UsersRepository import *
from python.Service.UsersService import *
users = UsersRepository()
result = users.insertUser(username ="Thanh2",password="02042003")
print(result)