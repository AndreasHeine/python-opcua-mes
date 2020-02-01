import mysql.connector, json

with open("pps.json") as file:
    pps = json.load(file)

mydb = mysql.connector.connect(
  host=pps["ip"],
  user=pps["user"],
  passwd=pps["password"],
  database=pps["dbname"]
)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM orders")

myresult = mycursor.fetchall()

for x in myresult:
  print(x)