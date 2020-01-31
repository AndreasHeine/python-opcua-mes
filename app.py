try:
    from opcua import ua, uamethod, Server
    from opcua.server.user_manager import UserManager
    import os, sys, json, sqlite3, time
    import asyncio
except ImportError as e:
    print(e)

project_folder = os.path.dirname(os.path.abspath(__file__))

with open("config.json") as file:
    config = json.load(file) 

debug = config["debug"]

with open("pps.json") as file:
    pps = json.load(file)

with open("users.json") as file:
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
def get_order(parent, id):
    global debug
    if debug:
        print(f"get order : {id}")
    #sqlite stuff here:
    #get next order from queue with highest prio
    return  (
                ua.Variant(id, ua.VariantType.Int64)
            )

@uamethod
def set_order_status(parent, id, status):
    global debug
    if debug:
        print(f"set order :{id} , {status}")
    #sqlite stuff here:
    #set order status
    #if failure return id + false
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
server.set_security_policy([ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt])
server.set_security_IDs(["Username"])
server.user_manager.set_user_manager(user_manager)

"""
OPC-UA-Modeling
"""
root_node = server.get_root_node()
object_node = server.get_objects_node()
server_node = server.get_server_node()

methods_obj = server.nodes.objects.add_object(address_space, "Methods")
get_order_node = methods_obj.add_method(    address_space, 
                                            "get_order", 
                                            get_order, 
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
    servicelevel_value = 0
    while True:
        await asyncio.sleep(1)
        if servicelevel_value < 200:
            servicelevel_value = 250
        servicelevel_dv = ua.DataValue(ua.Variant(servicelevel_value, ua.VariantType.Byte))
        servicelevel_node.set_value(servicelevel_dv)

loop = asyncio.get_event_loop()
asyncio.ensure_future(servicelevel_updater(server.get_node("ns=0;i=2267")))

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