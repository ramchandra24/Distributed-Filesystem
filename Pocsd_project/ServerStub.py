from SimpleXMLRPCServer import SimpleXMLRPCServer
import threading
import Memory_RPC as Memory
import config

class RaidServer():
    def __init__(self, server_port):
        server = SimpleXMLRPCServer(("localhost", server_port), allow_none=True)
        print "Listening on localhost : port ", server_port
        #Register all functions required for RPC
        server.register_instance(Memory.Operations())
        server.register_introspection_functions()
        #Start the server
        server.serve_forever()


server_port = config.SERVER_PORT_BEGIN
for server_num in range(config.NUM_OF_SERVERS):
    print "spawning server ", server_num
    server_handle = threading.Thread(target=RaidServer, args = (server_port, ))
    server_port = server_port + 1
    #server_handle.daemon = True
    server_handle.start()

for server_num in range(config.NUM_OF_SERVERS):
    server_handle.join();
    
print "All threads closed"