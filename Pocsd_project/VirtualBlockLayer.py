# Mapping functionalities
import config
import time
import MemoryInterface_RPC as Memory
filesystem = Memory.Operations()
#HANDLE FOR MEMORY OPERATIONS
class Operations():
    def __init__(self):
        self.vblock_mapper = {} # Dictionary to store Virtual -> Actual Block Number mapping
        self.numservers = config.NUM_OF_SERVERS
        self.client_blknum_counter = config.VIRTUAL_BLOCK_START
    
    #REQUEST TO BOOT THE FILE SYSTEM
    def Initialize_My_FileSystem(self):
        print("Filesystem Initializing......")
        for server_number in range(self.numservers):
            print("Disk " + str(server_number) + " initialized!")
            Memory.Initialize()
        print("Filesystem Initialized!")
        return


    #REQUEST TO FETCH THE INODE FROM INODE NUMBER FROM SERVER
    def inode_number_to_inode(self, inode_number):
        for server_number in range(self.numservers):
            inode = filesystem.inode_number_to_inode(server_number, inode_number)
            if inode:
                return inode
        return False


    #REQUEST THE DATA FROM THE SERVER
    def get_data_block(self, block_number):
        #self.print_vnodes()
        server1, block_num1 = self.get_server1_and_block_num(block_number)
        server2, block_num2 = self.get_server2_and_block_num(block_number)
        #parity_server, parity_block = self.vblock_mapper[block_number][config.PARITY_BLOCK]
        #for server_number, server_blknum in self.vblock_mapper[block_number].items():
        #    data = filesystem.get_data_block(server_number, server_blknum)
        #    if len(data) != 0: 
        #        return ''.join(data)
        data1 = []
        data2 = []

        data1.append(filesystem.get_data_block(server1, block_num1))
        data2.append(filesystem.get_data_block(server2, block_num2))

        ret_data = list(data1)

        if not data1:
            print ("Error VirtualBlockLayer: Server " + str(server1) + " not responding")
            ret_data = list(data2)
        if not data2:
            print ("Error VirtualBlockLayer: Server " + str(server2) + " not responding")
            ret_data = list(data1)

        if data1 != data2:
            print ("Error VirtualBlockLayer: Data on servers differ")
        return ''.join(ret_data)
        
        
    #REQUESTS THE VALID BLOCK NUMBER FROM THE SERVER 
    def get_valid_data_block(self):
        self.client_blknum_counter += 1
        #3 copies, 2 to store data and one for parity
        server_list = [None] * (config.REDUNDANCY_COUNT + 1)
        server_offset = self.client_blknum_counter % self.numservers
        serverA_number = server_offset
        serverB_number = (serverA_number + 1) % self.numservers
        parity_server_num = (serverB_number + 1) % self.numservers
        serverA_blknum = filesystem.get_valid_data_block(serverA_number)
        serverB_blknum = filesystem.get_valid_data_block(serverB_number)
        
        if -1 == serverA_blknum:
            print ("Error VirtualBlockLayer: Server " + str(serverA_number) + " not responding")
        if -1 == serverB_blknum:
            print ("Error VirtualBlockLayer: Server " + str(serverB_number) + " not responding")
        # Push a list of server numbers and block number mappings for each vblock
        server_list[config.DATA_BLOCK_1] = (serverA_number, serverA_blknum)
        server_list[config.DATA_BLOCK_2] = (serverB_number, serverB_blknum)
        
        # Create a mapping of Virtual Block Number with list of Actual Block Numbers and their servers
        self.vblock_mapper[self.client_blknum_counter] = server_list
        
        # Return the Virtual Block Number to the caller
        return self.client_blknum_counter
    
    def print_vnodes(self):
        print "Vnode size : ", len(self.vblock_mapper), " map:"
        for key, val in self.vblock_mapper.items():
            print key, " : ", val
        return

    def get_server1_and_block_num(self, block_number):
        #server, block_num = self.vblock_mapper[block_number][config.DATA_BLOCK_1]
        if block_number not in self.vblock_mapper:
            return (None, None)
        server_list = self.vblock_mapper[block_number]
        server, block_num = server_list[config.DATA_BLOCK_1]
        return (server, block_num)
    
    def get_server2_and_block_num(self, block_number):
        if block_number not in self.vblock_mapper:
            return (None, None)
        #server, block_num = self.vblock_mapper[block_number][config.DATA_BLOCK_2]
        server_list = self.vblock_mapper[block_number]
        server, block_num = server_list[config.DATA_BLOCK_2]
        return (server, block_num)


#REQUEST TO MAKE BLOCKS RESUABLE AGAIN FROM SERVER
    def free_data_block(self, vblock_number):
        serverA_number, serverA_blknum = self.get_server1_and_block_num(vblock_number)
        serverB_number, serverB_blknum = self.get_server2_and_block_num(vblock_number)
        # Delete the old Virtual block entry in the dictionary 
        if vblock_number in self.vblock_mapper:
            del self.vblock_mapper[vblock_number]
        
        status = filesystem.free_data_block(serverA_number, serverA_blknum)
        if -1 == status:
            print ("Error VirtualBlockLayer: Server " + str(serverA_number) + " not responding")
        status = filesystem.free_data_block(serverB_number, serverB_blknum)
        if -1 == status:
            print ("Error VirtualBlockLayer: Server " + str(serverB_number) + " not responding")

        return


    #REQUEST TO WRITE DATA ON THE THE SERVER
    def update_data_block(self, block_number, block_data):
        server1, block_num1 = self.get_server1_and_block_num(block_number)
        server2, block_num2 = self.get_server2_and_block_num(block_number)
        
        status = filesystem.update_data_block(server1, block_num1, block_data)
        if -1 == status:
            print ("Error VirtualBlockLayer: Server " + str(server1) + " not responding")
        status = filesystem.update_data_block(server2, block_num2, block_data)
        if -1 == status:
            print ("Error VirtualBlockLayer: Server " + str(server2) + " not responding")
        return
    
        


    #REQUEST TO UPDATE THE UPDATED INODE IN THE INODE TABLE FROM SERVER
    def update_inode_table(self, inode, inode_number):
        for server_number in range(self.numservers):
            filesystem.update_inode_table(server_number, inode, inode_number)
        return


    #REQUEST FOR THE STATUS OF FILE SYSTEM FROM SERVER
    def status(self):
        status = ""
        for server_number in range(self.numservers):
            status += str(server_number) + " : "
            status += filesystem.status(server_number)
        return status
