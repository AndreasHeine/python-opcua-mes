try:
    from opcua import ua, uamethod, Server
    from opcua.server.user_manager import UserManager
    import os, sys, json, sqlite3, time, random
    import asyncio
except ImportError as e:
    print(e)

project_folder = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(project_folder, "config.json")) as file:
    config = json.load(file) 

debug = config["debug"]

with open(os.path.join(project_folder, "pps.json")) as file:
    pps = json.load(file)

with open(os.path.join(project_folder, "users.json")) as file:
    users_db = json.load(file)

"""
OPC-UA-Usermanager
"""
def user_manager(isession, username, password):
    isession.user = UserManager.User
    return username in users_db and password == users_db[username]

"""
OPC-UA-Methods
"""
@uamethod
def get_next_order(parent, id):
    global debug
    if debug:
        print(f"get order : {id}")

    #get next order from queue
    #return id an detals
    #if empty return 0

    return  (
                ua.Variant(id, ua.VariantType.Int64)
            )

@uamethod
def set_order_status(parent, id, status):
    global debug
    if debug:
        print(f"set order :{id} , {status}")

    #update pps dataset
    #return id and error code (0=successful)
    #if fail: queue the unsend datasets

    error_code = 0
    return  (
                ua.Variant(id, ua.VariantType.Int64),
                ua.Variant(error_code, ua.VariantType.Int64)
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

status_obj = object_node.add_object(address_space, "Status")
queue_obj = status_obj.add_object(address_space, "Queue")
in_queue_size_node = queue_obj.add_variable(address_space, "size_in", ua.Variant(0, ua.VariantType.UInt64))
out_queue_size_node = queue_obj.add_variable(address_space, "size_out", ua.Variant(0, ua.VariantType.UInt64))

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

set_order_node = methods_obj.add_method(    address_space, 
                                            "set_order_status", 
                                            set_order_status, 
                                            [
                                                #Input-Arguments:
                                                ua.VariantType.Int64,
                                                ua.VariantType.Int64,
                                            ], 
                                            [
                                                #Output-Arguments:
                                                ua.VariantType.Int64,
                                                ua.VariantType.Int64,
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

async def in_queue_size_updater(in_queue_size_node):
    value = 5
    while True:
        await asyncio.sleep(1)
        in_queue_size_node.set_value(ua.DataValue(ua.Variant(value, ua.VariantType.UInt64)))

async def out_queue_size_updater(out_queue_size_node):
    value = 5
    while True:
        await asyncio.sleep(1)
        out_queue_size_node.set_value(ua.DataValue(ua.Variant(value, ua.VariantType.UInt64)))

async def random_updater(random_node):
    while True:
        await asyncio.sleep(random.randint(1,10))
        random_node.set_value(ua.DataValue(ua.Variant(random.randint(70,90), ua.VariantType.UInt64)))


loop = asyncio.get_event_loop()
asyncio.ensure_future(servicelevel_updater(server.get_node("ns=0;i=2267")))
asyncio.ensure_future(in_queue_size_updater(in_queue_size_node))
asyncio.ensure_future(out_queue_size_updater(out_queue_size_node))
asyncio.ensure_future(random_updater(random_node))

"""
OPC-UA-Server Start
"""
if __name__ == "__main__":
    print(f"Debug: { debug }")
    try:
        server.start()
        loop.run_forever()            
    except KeyboardInterrupt:
        loop.close()
        server.stop()
