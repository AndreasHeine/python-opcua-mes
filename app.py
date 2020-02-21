try:
    from opcua import ua, uamethod, Server
    from opcua.server.user_manager import UserManager
    import os, sys, json, sqlite3, time, random
    import asyncio
    import mysql.connector
except ImportError as e:
    print(e)

project_folder = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(project_folder, "config.json")) as file:
    config = json.load(file) 

debug = config["debug"]

"""
Production Planing System: mySQL database
"""
with open(os.path.join(project_folder, "pps.json")) as file:
    pps = json.load(file)

# pps_table = pps["table"]
# pps_db = mysql.connector.connect(
#                                 host=pps["ip"],
#                                 user=pps["user"],
#                                 passwd=pps["password"],
#                                 database=pps["dbname"]
#                                 )
# pps_cursor = pps_db.cursor()
# pps_db.disconnect()

"""
MES Order-Queue: SQLite3 database
"""
order_db = sqlite3.connect(':memory:')
order_cursor = order_db.cursor()
order_table = "order_queue"
order_cursor.execute(
                    f'''
                    CREATE TABLE {order_table}
                    (
                    order_id int,
                    status int
                    )
                    '''
                    )
order_db.commit()     

"""
OPC-UA-Usermanager
"""
with open(os.path.join(project_folder, "users.json")) as file:
    users_db = json.load(file)

def user_manager(isession, username, password):
    isession.user = UserManager.User
    return username in users_db and password == users_db[username]

"""
OPC-UA-Methods
"""
@uamethod
def get_next_order(parent, id):

    #get next order from queue
    #return id and details
    #if empty return 0

    return  (
                ua.Variant(id, ua.VariantType.Int64)
            )

"""
OPC-UA-Server Setup
"""
server = Server()
server.set_endpoint("opc.tcp://" + config["ip"] + ":" + config["port"])
server.set_server_name(config["servername"])
address_space = server.register_namespace(config["servername"] + config["endpointurl"])
server.set_application_uri(config["uri"])
server.load_certificate(config["cert"])
server.load_private_key(config["key"])
server.set_security_policy([ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt,ua.SecurityPolicyType.NoSecurity])
server.set_security_IDs(["Username"])
server.user_manager.set_user_manager(user_manager)

"""
OPC-UA-Modeling
"""
root_node = server.get_root_node()
object_node = server.get_objects_node()
server_node = server.get_server_node()

parameter_obj = object_node.add_object(address_space, "Parameter")
random_node = parameter_obj.add_variable(address_space, "random", ua.Variant(0, ua.VariantType.UInt64))

methods_obj = object_node.add_object(address_space, "Methods")
get_order_node = methods_obj.add_method(    address_space, 
                                            "get_next_order", 
                                            get_next_order, 
                                            [
                                                #Input-Arguments:
                                                ua.VariantType.Int64
                                            ], 
                                            [
                                                #Output-Arguments:
                                                ua.VariantType.Int64
                                            ]
                                        )

"""
OPC-UA-VarUpdater
"""
async def servicelevel_updater(servicelevel_node):
    value = 0
    while True:
        await asyncio.sleep(1)
        #no redundant servers!
        if value < 200:
            value = 250
            servicelevel_node.set_value(ua.DataValue(ua.Variant(value, ua.VariantType.Byte)))

async def random_updater(random_node):
    while True:
        await asyncio.sleep(random.randint(1,10))
        random_node.set_value(ua.DataValue(ua.Variant(random.randint(70,90), ua.VariantType.UInt64)))

async def order_queue_updater(db, table, pps):
    while True:
        await asyncio.sleep(0.1)
        #get pps database rows -> .fetchmany(queue_size)
        pps_table = pps["table"]
        #reconntect if fail
        pps_db = mysql.connector.connect(
                                        host=pps["ip"],
                                        user=pps["user"],
                                        passwd=pps["password"],
                                        database=pps["dbname"]
                                        )
        pps_cursor = pps_db.cursor(buffered=True)
        #maybe use yield
        pps_cursor.execute(
            f"""
            SELECT * FROM {pps_table}
            """
        )
        row = pps_cursor.fetchone() #row -> set
        #print(row)
        #write/update mes database
        #insert and commit!
        #if faile roleback pps
        
        #finaly
        if row:
            print(f"Order-ID {row[0]} Status: {row[1]}")
            order_id = str(row[0])
            pps_cursor.execute(
                f"""
                DELETE FROM {pps_table} WHERE order_id = {order_id}
                """
            )
            pps_db.commit()
        pps_db.disconnect()

            
loop = asyncio.get_event_loop()
asyncio.ensure_future(servicelevel_updater(server.get_node("ns=0;i=2267")))
asyncio.ensure_future(random_updater(random_node))
asyncio.ensure_future(order_queue_updater(order_db, order_table, pps))

"""
OPC-UA-Server Start
"""
if __name__ == "__main__":
    try:
        server.start()
        loop.run_forever()            
    except KeyboardInterrupt:
        loop.close()
        server.stop()