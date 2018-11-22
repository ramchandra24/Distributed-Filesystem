'''
THIS IS A MEMORY MODULE ON THE SREVER WHICH ACTS LIKE MEMORY OF FILE SYSTEM. ALL THE OPERATIONS REGARDING THE FILE SYSTEM OPERATES IN 
THIS MODULE. THE MODULE HAS POINTER TO DISK AND HAS EXACT SAME LAYOUT AS UNIX TYPE FILE SYSTEM.
'''  
import xmlrpclib as ClientRPC
from xmlrpclib import Fault as ClientError
import pickle as Serdes
from pickle import PickleError
from socket import error as SocketError
import config
numservers = config.NUM_OF_SERVERS

class Initialize():
    def __init__(self):
        print "Initializing memory on RPC"

#OPERATIONS ON FILE SYSTEM
class Operations():
    def __init__(self):
        #POINTER TO SERVER OBJECT
        self.startpoint = 8000
        self.memory_server = []
        try:
        	for i in range(self.startpoint, self.startpoint+numservers):        		
            	self.memory_server.append(ClientRPC.ServerProxy("http://localhost:" + str(i) + "/", allow_none=True))
        except (ClientError, SocketError) as error:
            print ("MemoryInterface_RPC Error: "), error
        #Catch other exceptions
        except Exception as error:
            print ("MemoryInterface_RPC Error: "), error

    #GIVES ADDRESS OF INODE TABLE
    def addr_inode_table(self):
        try:
            saddr_inode_blocks = self.memory_server.addr_inode_table()
            addr_inode_blocks = Serdes.loads(saddr_inode_blocks)
            return addr_inode_blocks
        except (ClientError, SocketError, PickleError) as error:
            print ("MemoryInterface_RPC Error: "), error
        #Catch other exceptions
        except Exception as error:
            print ("MemoryInterface_RPC Error: "), error
        return -1

    #RETURNS THE DATA OF THE BLOCK
    def get_data_block(self, server_number, block_number):
        try:
            sblock_number = Serdes.dumps(block_number)
            sdata_block = self.memory_server[server_number].get_data_block(sblock_number)
            data_block = Serdes.loads(sdata_block)
            return data_block
        except (ClientError, SocketError, PickleError) as error:
            print ("MemoryInterface_RPC Error: "), error
        #Catch other exceptions
        except Exception as error:
            print ("MemoryInterface_RPC Error: "), error
        return ""

    #RETURNS THE BLOCK NUMBER OF AVAIALBLE DATA BLOCK  
    def get_valid_data_block(self, server_number):
        try:
            sdata_block = self.memory_server[server_number].get_valid_data_block()
            data_block = Serdes.loads(sdata_block)
            return data_block
        except (ClientError, SocketError, PickleError) as error:
            print ("MemoryInterface_RPC Error: "), error
        #Catch other exceptions
        except Exception as error:
            print ("MemoryInterface_RPC Error: "), error
        return -1

    #REMOVES THE INVALID DATA BLOCK TO MAKE IT REUSABLE
    def free_data_block(self, server_number, block_number):
        try:
            sblock_number = Serdes.dumps(block_number)
            self.memory_server[server_number].free_data_block(sblock_number)
        except (ClientError, SocketError, PickleError) as error:
            print ("MemoryInterface_RPC Error: "), error
        #Catch other exceptions
        except Exception as error:
            print ("MemoryInterface_RPC Error: "), error
        return

    #WRITES TO THE DATA BLOCK
    def update_data_block(self, server_number, block_number, block_data):
        try:
            sblock_number = Serdes.dumps(block_number)
            sblock_data = Serdes.dumps(block_data)
            self.memory_server[server_number].update_data_block(sblock_number, sblock_data)
        except (ClientError, SocketError, PickleError) as error:
            print ("MemoryInterface_RPC Error: "), error
        #Catch other exceptions
        except Exception as error:
            print ("MemoryInterface_RPC Error: "), error
        return

    #UPDATES INODE TABLE WITH UPDATED INODE
    def update_inode_table(self, server_number, inode, inode_number):
        try:
            sinode = Serdes.dumps(inode)
            sinode_number = Serdes.dumps(inode_number)
            self.memory_server[server_number].update_inode_table(sinode, sinode_number)
        except (ClientError, SocketError, PickleError) as error:
            print ("MemoryInterface_RPC Error: "), error
        #Catch other exceptions
        except Exception as error:
            print ("MemoryInterface_RPC Error: "), error
        return

    #RETURNS THE INODE FROM INODE NUMBER
    def inode_number_to_inode(self, server_number, inode_number):
        try:
            sinode_number = Serdes.dumps(inode_number)
            saddr_inode_blocks = self.memory_server[server_number].inode_number_to_inode(sinode_number)
            addr_inode_blocks = Serdes.loads(saddr_inode_blocks)
            return addr_inode_blocks
        except (ClientError, SocketError, PickleError) as error:
            print ("MemoryInterface_RPC Error: "), error
        #Catch other exceptions
        except Exception as error:
            print ("MemoryInterface_RPC Error: "), error
        return False


    #SHOWS THE STATUS OF DISK LAYOUT IN MEMORY
    def status(self, server_number):
        try:
            sret_status = self.memory_server[server_number].status()
            ret_status = Serdes.loads(sret_status)
            return ret_status
        except (ClientError, SocketError, PickleError) as error:
            print ("MemoryInterface_RPC Error: "), error
        #Catch other exceptions
        except Exception as error:
            print ("MemoryInterface_RPC Error: "), error
        return ""

#------------------------------------------------------------ obj = Operations()
#------------------------------------------------ b = obj.get_valid_data_block()
#------------------------------------- obj.update_data_block(-1, "hello world!")
#------------------------------------------------------------ print obj.status()