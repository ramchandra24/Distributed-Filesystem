'''
THIS MODULE INTERACTS WITH THE MEMORY
''' 
#import time, Memory
import time
import xmlrpclib as ClientRPC
import pickle
#from xmlrpclib import ServerProxy as ClientRPC

#HANDLE FOR MEMORY OPERATIONS
#filesystem = Memory.Operations()


#------------------------------------------------------------------------------ 
#----------------------- proxy = ClientRPC.ServerProxy("http://localhost:8000/")
#--------------------------------- print "3 is even: %s" % str(proxy.is_even(3))
#----------------------------- print "100 is even: %s" % str(proxy.is_even(100))

Memory = ClientRPC.ServerProxy("http://localhost:8000/", allow_none=True)
methods = Memory.system.listMethods()
for method in methods:
    print method
try:
    pdata = [1, 2, 3, 4, 5]
    dat = pickle.dumps(pdata)
    ret = Memory.abcdef(dat)
    #state = Memory.Initialize.__init__()
    tab = Memory.status()
    print pickle.loads(tab)
except ClientRPC.Fault as err:
    print err
#filesystem = Memory.Operations.status()



#REQUEST TO BOOT THE FILE SYSTEM
def Initialize_My_FileSystem():
    print("File System Initializing......")
    time.sleep(2)
    #state = Memory.Initialize()
    print("File System Initialized!")


#REQUEST TO FETCH THE INODE FROM INODE NUMBER FROM SERVER
def inode_number_to_inode(inode_number):
    return filesystem.inode_number_to_inode(inode_number)


#REQUEST THE DATA FROM THE SERVER
def get_data_block(block_number):
    return ''.join(filesystem.get_data_block(block_number))


#REQUESTS THE VALID BLOCK NUMBER FROM THE SERVER 
def get_valid_data_block():
    return ( filesystem.get_valid_data_block() )


#REQUEST TO MAKE BLOCKS RESUABLE AGAIN FROM SERVER
def free_data_block(block_number):
    filesystem.free_data_block((block_number))


#REQUEST TO WRITE DATA ON THE THE SERVER
def update_data_block(block_number, block_data):
    filesystem.update_data_block(block_number, block_data)


#REQUEST TO UPDATE THE UPDATED INODE IN THE INODE TABLE FROM SERVER
def update_inode_table(inode, inode_number):
    filesystem.update_inode_table(inode, inode_number)


#REQUEST FOR THE STATUS OF FILE SYSTEM FROM SERVER
def status():
    return filesystem.status()