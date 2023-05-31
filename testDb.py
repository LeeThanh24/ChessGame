import mysql.connector
db= mysql.connector.connect(user= 'root',password = '02042003',host='localhost',database = 'Chess')
query = "INSERT INTO users VALUES  (1,'Thanh','02042003',100) "
query = "select * from users"
cursor = db.cursor()
cursor.execute(query)
result = cursor.fetchall()
print (result)

