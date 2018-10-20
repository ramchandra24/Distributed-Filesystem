from SimpleXMLRPCServer import SimpleXMLRPCServer
import Memory_RPC as Memory

server = SimpleXMLRPCServer(("localhost", 8000), allow_none=True)
print "Listening on localhost : port 8000"
#Register all functions required for RPC
server.register_instance(Memory.Operations())
server.register_introspection_functions()

#Start the server
server.serve_forever()


