import mysql.connector, json, random
import os

project_folder = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(project_folder, "pps.json")) as file:
    pps = json.load(file)

mydb = mysql.connector.connect(
  host=pps["ip"],
  user=pps["user"],
  passwd=pps["password"],
  database=pps["dbname"]
)

mycursor = mydb.cursor()

try:
    mycursor.execute(
                    """
                        DROP TABLE orders;
                    """
                    )
    mydb.commit()

    print("Table Droped!")
except:
    pass

mycursor.execute(
                f"""
                CREATE TABLE {pps["table"]} 
                    (
                    order_id int,
                    status int
                    );
                """
                )
mydb.commit()
print("Table Created!")


for i in range(1,100000):
    r = random.randint(1,5000)
    mycursor.execute(
                    f"""
                        INSERT INTO orders (order_id,status)
                        VALUES ({i},{r});
                    """
                    )

mydb.commit()
print("Orders Created!")