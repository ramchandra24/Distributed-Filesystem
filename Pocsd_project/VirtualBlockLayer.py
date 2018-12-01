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
        self.num_data_servers = config.NUM_OF_DATA_SERVERS
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
        server1, block_num1 = self.get_server1_and_block_num(block_number)
        server2, block_num2 = self.get_server2_and_block_num(block_number)
        parity_server, parity_blknum = self.get_parity_server_and_block_num(block_number)
        #parity_server, parity_block = self.vblock_mapper[block_number][config.PARITY_BLOCK]
        #for server_number, server_blknum in self.vblock_mapper[block_number].items():
        #    data = filesystem.get_data_block(server_number, server_blknum)
        #    if len(data) != 0: 
        #        return ''.join(data)

        data1 = []
        data2 = []
        parity = []

        data1.append(filesystem.get_data_block(server1, block_num1))
        data2.append(filesystem.get_data_block(server2, block_num2))
        parity.append(filesystem.get_data_block(parity_server, parity_blknum))

        ret_data = list(data1)

        if not data1:
            print ("Error VirtualBlockLayer: Server " + str(server1) + " not responding")
            ret_data = list(data2)
        if not data2:
            print ("Error VirtualBlockLayer: Server " + str(server2) + " not responding")
            ret_data = list(data1)
        if not parity:
            print ("Error VirtualBlockLayer: Parity Server " + str(server2) + " not responding")
        
        if data1 != data2:
            print ("Error VirtualBlockLayer: Data on servers differ")
        
        return ''.join(ret_data)

    #REQUESTS THE VALID BLOCK NUMBER FROM THE SERVER 
    def get_valid_data_block(self):
        self.client_blknum_counter += 1
        #3 copies, 2 to store data and one for parity
        server_list = [None] * (config.REDUNDANCY_COUNT + 1)
        server_offset = self.client_blknum_counter % self.num_data_servers
        
        serverA_number = server_offset
        serverB_number = (serverA_number + 1) % self.num_data_servers
        parity_server_num = config.NUM_OF_SERVERS - 1
        
        serverA_blknum = filesystem.get_valid_data_block(serverA_number)
        serverB_blknum = filesystem.get_valid_data_block(serverB_number)
        parity_blknum = filesystem.get_valid_data_block(parity_server_num)
        
        if -1 == serverA_blknum:
            print ("Error VirtualBlockLayer: Server " + str(serverA_number) + " not responding")
        if -1 == serverB_blknum:
            print ("Error VirtualBlockLayer: Server " + str(serverB_number) + " not responding")
        if -1 == parity_blknum:
            print ("Error VirtualBlockLayer: Server " + str(parity_server_num) + " not responding")

        # Push a list of server numbers and block number mappings for each vblock
        server_list[config.DATA_BLOCK_1] = (serverA_number, serverA_blknum)
        server_list[config.DATA_BLOCK_2] = (serverB_number, serverB_blknum)
        server_list[config.PARITY_BLOCK] = (parity_server_num, parity_blknum)
        
        # Create a mapping of Virtual Block Number with list of Actual Block Numbers and their servers
        # Add the new Virtual block -> Actual block mapping to the dictionary
        self.vblock_mapper[self.client_blknum_counter] = server_list
        
        # Return the Virtual Block Number to the caller
        return self.client_blknum_counter
    
    def print_vnodes(self):
        print "Vnode size : ", len(self.vblock_mapper), " map:"
        for key, val in self.vblock_mapper.items():
            print key, " : ", val
        return

    def get_server1_and_block_num(self, block_number):
        self.print_vnodes()
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
    
    def get_parity_server_and_block_num(self, block_number):
        if block_number not in self.vblock_mapper:
            return (None, None)
        #server, block_num = self.vblock_mapper[block_number][config.DATA_BLOCK_2]
        server_list = self.vblock_mapper[block_number]
        server, block_num = server_list[config.PARITY_BLOCK]
        return (server, block_num)

    #REQUEST TO MAKE BLOCKS RESUABLE AGAIN FROM SERVER
    def free_data_block(self, vblock_number):
        serverA_number, serverA_blknum = self.get_server1_and_block_num(vblock_number)
        serverB_number, serverB_blknum = self.get_server2_and_block_num(vblock_number)
        parity_server_num, parity_blknum = self.get_parity_server_and_block_num(vblock_number)
        
        # Delete the old Virtual block entry in the dictionary 
        if vblock_number in self.vblock_mapper:
            del self.vblock_mapper[vblock_number]
        
        status = filesystem.free_data_block(serverA_number, serverA_blknum)
        if -1 == status:
            print ("Error VirtualBlockLayer: Server " + str(serverA_number) + " not responding")
        status = filesystem.free_data_block(serverB_number, serverB_blknum)
        if -1 == status:
            print ("Error VirtualBlockLayer: Server " + str(serverB_number) + " not responding")
        status = filesystem.free_data_block(parity_server_num, parity_blknum)
        if -1 == status:
            print ("Error VirtualBlockLayer: Server " + str(parity_server_num) + " not responding")

        return

    
    #UPDATED PARITY DATA
    def get_parity_data(self, vblock_number, block_data):
        parity_server_num, parity_blknum = self.get_parity_server_and_block_num(vblock_number)
        parity_block_data = filesystem.get_data_block(parity_server_num, parity_blknum)
        
        if parity_block_data[0] == '\0':
            curr_parity_data = [0] * config.BLOCK_SIZE
        else:
            curr_parity_data = map(int, block_data)
        
        updated_parity_data = curr_parity_data
        
        int_block_data = []
        for i in range(len(block_data)):
           int_block_data.append(ord(block_data[i]))
        for i in range(len(block_data), config.BLOCK_SIZE):
            int_block_data.append(0)

        for i in range(len(curr_parity_data)):
            updated_parity_data[i] = curr_parity_data[i] ^ int_block_data[i]
        
        new_updated_parity = updated_parity_data
        
        for i in range(len(updated_parity_data)):
            if updated_parity_data[i] != 0:
                new_updated_parity[i] = chr(updated_parity_data[i])
            else:
                new_updated_parity[i] = '\0'
        return ''.join(new_updated_parity)
    
    #REQUEST TO WRITE DATA ON THE THE SERVER
    def update_data_block(self, vblock_number, block_data):
        server1, block_num1 = self.get_server1_and_block_num(vblock_number)
        server2, block_num2 = self.get_server2_and_block_num(vblock_number)
        parity_server, parity_blknum = self.get_parity_server_and_block_num(vblock_number)
        
        status = filesystem.update_data_block(server1, block_num1, block_data)
        if -1 == status:
            print ("Error VirtualBlockLayer: Server " + str(server1) + " not responding")
        status = filesystem.update_data_block(server2, block_num2, block_data)
        if -1 == status:
            print ("Error VirtualBlockLayer: Server " + str(server2) + " not responding")
            
        parity_data = self.get_parity_data(vblock_number, block_data)
        status = filesystem.update_data_block(parity_server, parity_blknum, parity_data)
        print filesystem.status(parity_server)
        if -1 == status:
            print ("Error VirtualBlockLayer: Server " + str(server2) + " not responding")
        
        return
    
    
    #REQUEST TO UPDATE THE UPDATED INODE IN THE INODE TABLE FROM SERVER
    def update_inode_table(self, inode, inode_number):
        #self.print_vnodes()
        for server_number in range(self.numservers):
            filesystem.update_inode_table(server_number, inode, inode_number)
        return


    #REQUEST FOR THE STATUS OF FILE SYSTEM FROM SERVER
    def status(self):
        status = ""
        for server_number in range(self.num_data_servers):
            status += str(server_number) + " : "
            status += filesystem.status(server_number)
        return status


#------------------------------------------------------------ obj = Operations()
#------------------------------------------------ obj.Initialize_My_FileSystem()
#------------------------------------------------ b = obj.get_valid_data_block()
#-------------------------------------- obj.update_data_block(b, "hello world!")
#print obj.status()