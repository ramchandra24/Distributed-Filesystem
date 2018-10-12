'''
THIS IS A MEMORY MODULE ON THE SREVER WHICH ACTS LIKE MEMORY OF FILE SYSTEM. ALL THE OPERATIONS REGARDING THE FILE SYSTEM OPERATES IN 
THIS MODULE. THE MODULE HAS POINTER TO DISK AND HAS EXACT SAME LAYOUT AS UNIX TYPE FILE SYSTEM.
'''  
import xmlrpclib as ServerRPC
from SimpleXMLRPCServer import SimpleXMLRPCServer
import pickle as Serdes
import Memory

#OPERATIONS ON FILE SYSTEM
class Operations():
    def __init__(self):
        #POINTER TO MEMORY OBJECT
        Memory.Initialize()
        self.memory_obj = Memory.Operations()

    #GIVES ADDRESS OF INODE TABLE
    def addr_inode_table(self):
        addr_inode_blocks = self.memory_obj.addr_inode_table()
        print addr_inode_blocks
        return addr_inode_blocks

    #RETURNS THE DATA OF THE BLOCK
    def get_data_block(self, sblock_number):
        block_number = Serdes.loads(sblock_number)
        data_block = self.memory_obj.get_data_block(block_number)
        sdata_block = Serdes.dumps(data_block)
        return sdata_block

    #RETURNS THE BLOCK NUMBER OF AVAIALBLE DATA BLOCK  
    def get_valid_data_block(self):
        data_block = self.memory_obj.get_valid_data_block()
        sdata_block = Serdes.dumps(data_block)
        return sdata_block

    #REMOVES THE INVALID DATA BLOCK TO MAKE IT REUSABLE
    def free_data_block(self, sblock_number):
        block_number = Serdes.loads(sblock_number)
        self.memory_obj.free_data_block(block_number)
        return

    #WRITES TO THE DATA BLOCK
    def update_data_block(self, sblock_number, sblock_data):
        block_number = Serdes.loads(sblock_number)
        block_data = Serdes.loads(sblock_data)
        self.memory_obj.update_data_block(block_number, block_data)

    #UPDATES INODE TABLE WITH UPDATED INODE
    def update_inode_table(self, sinode, sinode_number):
        inode = Serdes.loads(sinode)
        inode_number = Serdes.loads(sinode_number)
        self.memory_obj.update_inode_table(inode, inode_number)

    #RETURNS THE INODE FROM INODE NUMBER
    def inode_number_to_inode(self, sinode_number):
        inode_number = Serdes.loads(sinode_number)
        addr_inode_blocks = self.memory_obj.inode_number_to_inode(inode_number)
        saddr_inode_blocks = Serdes.dumps(addr_inode_blocks)
        return saddr_inode_blocks

    #SHOWS THE STATUS OF DISK LAYOUT IN MEMORY
    def status(self):
        ret_status = self.memory_obj.status()
        sret_status = Serdes.dumps(ret_status)
        #return sret_status
        return "\\"


server = SimpleXMLRPCServer(("localhost", 8000), allow_none=True)
print "Listening on port 8000..."
server.register_instance(Operations())
server.register_introspection_functions()
server.serve_forever()


