from SimpleXMLRPCServer import SimpleXMLRPCServer
import threading
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


#server_port = config.SERVER_PORT_BEGIN
server_port = 8000

server = RaidServer(server_port)
server_handle = server.start_server()

inp = raw_input("Enter k to kill")
while 'k' != inp:
    inp = raw_input()

#kill the server
server.shutdown_server()


    
print "Server ", server_port, " Shutdown"