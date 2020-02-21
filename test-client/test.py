from opcua import Client, ua

class SubHandler(object):

    """
    Subscription Handler. To receive events from server for a subscription
    data_change and event methods are called directly from receiving thread.
    Do not do expensive, slow or network operation there. Create another 
    thread if you need to do such a thing
    """

    def datachange_notification(self, node, val, data):
        print("Python: New data change event", node, val)

    def event_notification(self, event):
        print("Python: New event", event)


if __name__ == "__main__":
    client = Client("opc.tcp://127.0.0.1:4840")
    client.connect()
    client.load_type_definitions()

    uri = "Python-OPC-UA/"
    idx = client.get_namespace_index(uri)
    print(idx)

    root = client.get_root_node()
    objects = client.get_objects_node()

    myvar = root.get_child(["0:Objects", "{}:Parameter".format(idx), "{}:random".format(idx)])

    handler = SubHandler()
    sub = client.create_subscription(500, handler)
    handle = sub.subscribe_data_change(myvar)