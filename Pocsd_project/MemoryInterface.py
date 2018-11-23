'''
THIS MODULE INTERACTS WITH THE MEMORY
''' 
import time
import MemoryInterface_RPC as Memory

class MemoryInterface():
    def __init__(self, server_num):
        #HANDLE FOR MEMORY OPERATIONS
        self.filesystem = Memory.Operations(server_num)
        #Initialize_My_FileSystem()
        
    #REQUEST FOR THE STATUS OF FILE SYSTEM FROM SERVER
    def status(self):
        return self.filesystem.status()

    #REQUEST TO BOOT THE FILE SYSTEM
    def Initialize_My_FileSystem(self):
        print("File System Initializing......")
        time.sleep(2)
        self.filesystem.Initialize()
        print("File System Initialized!")
    
    
    #REQUEST TO FETCH THE INODE FROM INODE NUMBER FROM SERVER
    def inode_number_to_inode(self, inode_number):
        return self.filesystem.inode_number_to_inode(inode_number)
    
    
    #REQUEST THE DATA FROM THE SERVER
    def get_data_block(self, block_number):
        return ''.join(self.filesystem.get_data_block(block_number))
    
    
    #REQUESTS THE VALID BLOCK NUMBER FROM THE SERVER 
    def get_valid_data_block(self):
        return ( self.filesystem.get_valid_data_block() )
    
    
    #REQUEST TO MAKE BLOCKS RESUABLE AGAIN FROM SERVER
    def free_data_block(self, block_number):
        self.filesystem.free_data_block((block_number))
    
    
    #REQUEST TO WRITE DATA ON THE THE SERVER
    def update_data_block(self, block_number, block_data):
        self.filesystem.update_data_block(block_number, block_data)
    
    
    #REQUEST TO UPDATE THE UPDATED INODE IN THE INODE TABLE FROM SERVER
    def update_inode_table(self, inode, inode_number):
        self.filesystem.update_inode_table(inode, inode_number)


a = MemoryInterface(8000)
b = MemoryInterface(8001)

ablock = a.get_valid_data_block()
print "a block number", ablock
a.update_data_block(ablock, "server 1")
print a.status()

bblock = b.get_valid_data_block()
print "b block number", bblock
b.update_data_block(bblock, "server 2")

#print a.status()
print b.status()
