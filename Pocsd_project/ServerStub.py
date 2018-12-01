from SimpleXMLRPCServer import SimpleXMLRPCServer
import threading
from multiprocessing import Process
import Memory_RPC as Memory
import config

class RaidServer():
    def __init__(self, server_port):
        self.memory = Memory.Operations()
        self.server = SimpleXMLRPCServer(("localhost", server_port), allow_none=True)
        print "Listening on localhost : port ", server_port
        #Register all functions required for RPC
        self.server.register_instance(self.memory)
        self.server.register_introspection_functions()
        return
        
    def start_server(self):
        #Start the server
        self.server.serve_forever()
        
    def shutdown_server(self):
        #Shutdown the server
        self.shutdown_server()


server_port = config.SERVER_PORT_BEGIN
#server_port = 8003
server_handle = [None] * (config.NUM_OF_SERVERS)
server_arr = [None] * (config.NUM_OF_SERVERS)
for server_num in range(config.NUM_OF_SERVERS):
    print "spawning server ", server_num
    server = RaidServer(server_port)
    server_arr[server_num] = server
    server_handle[server_num] = threading.Thread(target=server.start_server, args = ( ))
    #server_handle[server_num] = Process(target = server.start_server, args=())
    #server_handle[server_num].daemon = True
    server_port += 1
    #server_handle.daemon = True
    #server_handle[server_num].start()

for server_num in range(config.NUM_OF_SERVERS):
    #server_handle[server_num].server_close();
    server_handle[server_num].start()
    

inpS = -1
try:
    inpS = int(raw_input("Kill one server?"))
    server_arr[inpS].shutdown_server()
    server_handle[server_num].running = False
except:
    print "Killing all servers"

inp = raw_input("Enter k to kill")
while 'k' != inp:
    inp = raw_input()

for server_num in range(config.NUM_OF_SERVERS):
     if server_num == inpS: continue
     #server_handle[server_num].server_close();
     server_arr[server_num].shutdown_server()
     server_handle[server_num].running = False


for server_num in range(config.NUM_OF_SERVERS):
    #server_handle[server_num].server_close();
    server_handle[server_num].join()

#for server_num in range(config.NUM_OF_SERVERS):
#    server_handle.join();
    
print "All Servers Shutdown"