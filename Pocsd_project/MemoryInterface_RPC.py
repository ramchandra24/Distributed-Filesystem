'''
THIS IS A MEMORY MODULE ON THE SREVER WHICH ACTS LIKE MEMORY OF FILE SYSTEM. ALL THE OPERATIONS REGARDING THE FILE SYSTEM OPERATES IN 
THIS MODULE. THE MODULE HAS POINTER TO DISK AND HAS EXACT SAME LAYOUT AS UNIX TYPE FILE SYSTEM.
'''  
import xmlrpclib as ClientRPC
from xmlrpclib import Fault as ClientError
import pickle as Serdes
from pickle import PickleError
from socket import error as SocketError

class Initialize():
    def __init__(self):
        print "Initializing memory on RPC"
        return

#OPERATIONS ON FILE SYSTEM
class Operations():
    def __init__(self):
        #POINTER TO SERVER OBJECT
        try:
            self.memory_server = ClientRPC.ServerProxy("http://localhost:8000/", allow_none=True)
        except (ClientError, SocketError) as error:
            print ("MemoryInterface_RPC Error: "), error
        #Catch other exceptions
        except Exception as error:
            print ("MemoryInterface_RPC Error: "), error

    #GIVES ADDRESS OF INODE TABLE
    def addr_inode_table(self):
        try:
            addr_inode_blocks = self.memory_server.addr_inode_table()
            return addr_inode_blocks
        except (ClientError, SocketError) as error:
            print ("MemoryInterface_RPC Error: "), error
        #Catch other exceptions
        except Exception as error:
            print ("MemoryInterface_RPC Error: "), error
        return -1

    #RETURNS THE DATA OF THE BLOCK
    def get_data_block(self, block_number):
        try:
            sblock_number = Serdes.dumps(block_number)
            sdata_block = self.memory_server.get_data_block(sblock_number)
            data_block = Serdes.loads(sdata_block)
            return data_block
        except (ClientError, SocketError, PickleError) as error:
            print ("MemoryInterface_RPC Error: "), error
        #Catch other exceptions
        except Exception as error:
            print ("MemoryInterface_RPC Error: "), error
        return ""

    #RETURNS THE BLOCK NUMBER OF AVAIALBLE DATA BLOCK  
    def get_valid_data_block(self):
        try:
            sdata_block = self.memory_server.get_valid_data_block()
            data_block = Serdes.loads(sdata_block)
            return data_block
        except (ClientError, SocketError) as error:
            print ("MemoryInterface_RPC Error: "), error
        return -1

    #REMOVES THE INVALID DATA BLOCK TO MAKE IT REUSABLE
    def free_data_block(self, block_number):
        try:
            sblock_number = Serdes.dumps(block_number)
            self.memory_server.free_data_block(sblock_number)
        except (ClientError, SocketError, PickleError) as error:
            print ("MemoryInterface_RPC Error: "), error
        return

    #WRITES TO THE DATA BLOCK
    def update_data_block(self, block_number, block_data):
        try:
            sblock_number = Serdes.dumps(block_number)
            sblock_data = Serdes.dumps(block_data)
            self.memory_server.update_data_block(sblock_number, sblock_data)
        except (ClientError, SocketError, PickleError) as error:
            print ("MemoryInterface_RPC Error: "), error
        return

    #UPDATES INODE TABLE WITH UPDATED INODE
    def update_inode_table(self, inode, inode_number):
        try:
            sinode = Serdes.dumps(inode)
            sinode_number = Serdes.dumps(inode_number)
            self.memory_server.update_inode_table(sinode, sinode_number)
        except (ClientError, SocketError, PickleError) as error:
            print ("MemoryInterface_RPC Error: "), error
        return

    #RETURNS THE INODE FROM INODE NUMBER
    def inode_number_to_inode(self, inode_number):
        try:
            sinode_number = Serdes.dumps(inode_number)
            saddr_inode_blocks = self.memory_server.inode_number_to_inode(sinode_number)
            addr_inode_blocks = Serdes.loads(saddr_inode_blocks)
            return addr_inode_blocks
        except (ClientError, SocketError, PickleError) as error:
            print ("MemoryInterface_RPC Error: "), error
        return -1


    #SHOWS THE STATUS OF DISK LAYOUT IN MEMORY
    def status(self):
        try:
            sret_status = self.memory_server.status()
            ret_status = Serdes.loads(sret_status)
            return ret_status
        except (ClientError, SocketError, PickleError) as error:
            print ("MemoryInterface_RPC Error: "), error
        #Catch other exceptions
        except Exception as error:
            print ("MemoryInterface_RPC Error: "), error
        return ""

obj = Operations()
print obj.status()