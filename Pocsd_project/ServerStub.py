from SimpleXMLRPCServer import SimpleXMLRPCServer
import threading
import subprocess
import Memory_RPC as Memory
import config

class RaidServer():
    def __init__(self, server_port):
        #self.memory = Memory.Operations()
        self.server = SimpleXMLRPCServer(("localhost", server_port), allow_none=True)
        print "Listening on localhost : port ", server_port
        #Register all functions required for RPC
        self.server.register_instance(Memory.Operations())
        self.server.register_introspection_functions()
        return
        
    def start_server(self):
        #Start the server
        self.server.serve_forever()


server_port = config.SERVER_PORT_BEGIN
server_handle = [None] * config.NUM_OF_SERVERS
for server_num in range(config.NUM_OF_SERVERS):
    print "spawning server ", server_num
    server = RaidServer(server_port)
    #server_handle[server_num] = threading.Thread(target=RaidServer, args = (server_port, ))
    server_handle[server_num] = subprocess.Popen(server.start_server())
    server_port = server_port + 1
    #server_handle.daemon = True
    #server_handle[server_num].start()

for server_num in range(config.NUM_OF_SERVERS):
    #server_handle[server_num].server_close();
    server_handle[server_num].subprocess.wait()


#for server_num in range(config.NUM_OF_SERVERS):
#    server_handle.join();
    
print "All Servers Shutdown"