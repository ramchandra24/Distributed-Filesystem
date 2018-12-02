# Mapping functionalities
import config
import time
import MemoryInterface_RPC as Memory

filesystem = Memory.Operations()
#HANDLE FOR MEMORY OPERATIONS
class Operations():
    def __init__(self):
        self.vblock_mapper = {} # Dictionary to store Virtual -> Actual Block Number mapping
        self.parity_mapper = {} # Dictionary to store Virtual -> Actual Block Number mapping for parity disk
        self.numservers = config.NUM_OF_SERVERS
        self.num_data_servers = config.NUM_OF_DATA_SERVERS
        self.client_blknum_counter = config.VIRTUAL_BLOCK_START
    
    #REQUEST TO BOOT THE FILE SYSTEM
    def Initialize_My_FileSystem(self):
        print("Filesystem Initializing......")
        for server_number in range(self.numservers):
            print("Initializing Disk " + str(server_number))
            Memory.Initialize()
        filesystem.Initialize_My_FileSystem()
        print("Filesystem Initialized!")
        return


    #REQUEST TO FETCH THE INODE FROM INODE NUMBER FROM SERVER
    def inode_number_to_inode(self, inode_number):
        for server_number in range(self.numservers):
            inode = filesystem.inode_number_to_inode(server_number, inode_number)
            if inode:
                return inode
        return False


    def xor_block_data(self, block1_data, block2_data):
        int_block1_data = []
        for i in range(len(block1_data)):
           int_block1_data.append(ord(block1_data[i]))
        for i in range(len(block1_data), config.BLOCK_SIZE):
            int_block1_data.append(0)
        
        int_block2_data = []
        for i in range(len(block2_data)):
           int_block2_data.append(ord(block2_data[i]))
        for i in range(len(block2_data), config.BLOCK_SIZE):
            int_block2_data.append(0)

        int_xored_block = [0] * config.BLOCK_SIZE
        for i in range(config.BLOCK_SIZE):
            int_xored_block[i] = int_block1_data[i] ^ int_block2_data[i]
        
        xored_block = ['\0'] * config.BLOCK_SIZE
        
        for i in range(config.BLOCK_SIZE):
            if int_xored_block[i] != 0:
                xored_block[i] = chr(int_xored_block[i])
        #print "parity data str ", new_updated_parity
        return ''.join(xored_block)


    def correct_data_from_parity_server(self, faulty_server, block_number):
        parity_server_num = config.NUM_OF_SERVERS - 1
        if block_number in self.parity_mapper:
            print "Parity to the rescue"
            parity_blknum = self.parity_mapper[block_number]
        else:
            print "Doomed bro. Parity can't help"
            return
        
        parity_block_data = filesystem.get_data_block(parity_server_num, parity_blknum)
        recovered_block_data = parity_block_data
        for i in range(self.num_data_servers):
            if i == faulty_server : continue
            data_block = filesystem.get_data_block(i, block_number)
            recovered_block_data = self.xor_block_data(recovered_block_data, data_block)
        
        return ''.join(recovered_block_data)
        

    #REQUEST THE DATA FROM THE SERVER
    def get_data_block(self, block_number):
        #self.print_vnodes()
        server1, block_num1 = self.get_server1_and_block_num(block_number)
        #server2, block_num2 = self.get_server2_and_block_num(block_number)
        #parity_server, parity_blknum = self.get_parity_server_and_block_num(block_number)
        #print "Read from Data Servers : ", server1, ", ",  server2
        stime = config.SLEEP_TIME
        print "waiting ", stime, " seconds before first read"
        time.sleep(stime)
        ret_data = ''
        
        print "Reading from Server: ", server1
        data1 = filesystem.get_data_block(server1, block_num1)
        
        print data1
        # if nothing was returned from server 1 try server 2
        if data1 == '':
            print "Server ", server1, " not responding"
            print "Correcting data with parity server"
            data1 = self.correct_data_from_parity_server(server1, block_num1)
        
        ret_data = data1
        
        #print "waiting ", stime, " seconds before second read"
        #time.sleep(stime)
        
        #print "Reading from Server: ", server2
        #ret_data2 = ''
        #data2 = filesystem.get_data_block(server2, block_num2)
        #ret_data2 = data2
        
        #if data2 == '':
        #    print "Server ", server2, " not responding"
        
        #if ret_data1 == '':
        #    ret_data = ret_data2
        #else:
        #    ret_data = ret_data1

        return ''.join(ret_data)

    #REQUESTS THE VALID BLOCK NUMBER FROM THE SERVER 
    def get_valid_data_block(self):
        self.client_blknum_counter += 1
        #3 copies, 2 to store data and one for parity
        server_list = [None] * (config.REDUNDANCY_COUNT)
        server_offset = self.client_blknum_counter % self.num_data_servers
        
        serverA_number = server_offset
        #serverB_number = (serverA_number + 1) % self.num_data_servers
        #parity_server_num = config.NUM_OF_SERVERS - 1
        
        serverA_blknum = filesystem.get_valid_data_block(serverA_number)
        #serverB_blknum = filesystem.get_valid_data_block(serverB_number)
        #parity_blknum = filesystem.get_valid_data_block(parity_server_num)
        
        if -1 == serverA_blknum:
            #print ("Error VirtualBlockLayer: Server " + str(serverA_number) + " not responding")
            serverA_number = (serverB_number + 1) % self.numservers
            serverA_blknum = filesystem.get_valid_data_block(serverA_number)
            #serverA_number = None
        #---------------------------------------------- if -1 == serverB_blknum:
            # #print ("Error VirtualBlockLayer: Server " + str(serverB_number) + " not responding")
            #----------- serverB_number = (serverB_number + 1) % self.numservers
            #-- serverB_blknum = filesystem.get_valid_data_block(serverB_number)
       
        #----------------------------------------------- if -1 == parity_blknum:
            # print ("Error VirtualBlockLayer: Server " + str(parity_server_num) + " not responding")

        # Push a list of server numbers and block number mappings for each vblock
        server_list[config.DATA_BLOCK_1] = (serverA_number, serverA_blknum)
        #server_list[config.DATA_BLOCK_2] = (serverB_number, serverB_blknum)
        
        
        #server_list[config.PARITY_BLOCK] = (parity_server_num, parity_blknum)
        #------------------------------- if serverA_blknum not in parity_mapper:
            #--------------- self.parity_mapper[serverA_blknum] = serverA_blknum
        #--------------------------------------------------- self.print_pnodes()
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
    
    def print_pnodes(self):
        print "Pnode size : ", len(self.parity_mapper), " map:"
        for key, val in self.parity_mapper.items():
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
        #serverB_number, serverB_blknum = self.get_server2_and_block_num(vblock_number)
        #parity_server_num, parity_blknum = self.get_parity_server_and_block_num(vblock_number)
        
        status = 0
        #print "Delete block from Data Servers: ", serverA_number, ", ", serverB_number
        if None != serverA_number:
            status = filesystem.free_data_block(serverA_number, serverA_blknum)
        if -1 == status:
            print ("Error VirtualBlockLayer: Server " + str(serverA_number) + " not responding")
        #-------------------------------------------- if None != serverB_number:
            # status = filesystem.free_data_block(serverB_number, serverB_blknum)
        #------------------------------------------------------ if -1 == status:
            # print ("Error VirtualBlockLayer: Server " + str(serverB_number) + " not responding")
        #- status = filesystem.free_data_block(parity_server_num, parity_blknum)
        #------------------------------------------------------ if -1 == status:
            # print ("Error VirtualBlockLayer: Server " + str(parity_server_num) + " not responding")

        # Delete the old Virtual block entry in the dictionary 
        if vblock_number in self.vblock_mapper:
            del self.vblock_mapper[vblock_number]
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
    
    #UPDATED PARITY DATA
    def update_parity_data(self, block_number, block_data):
        print "Updating parity for block ", block_number
        parity_server_num = config.NUM_OF_SERVERS - 1
        if block_number in self.parity_mapper:
            parity_blknum = self.parity_mapper[block_number]
        else:
            parity_blknum = filesystem.get_valid_data_block(parity_server_num)
            self.parity_mapper[block_number] = parity_blknum
        
        parity_block_data = filesystem.get_data_block(parity_server_num, block_number)
        
        #if parity_block_data[0] == '\0':
        #    curr_parity_data = [0] * config.BLOCK_SIZE
        #else:
        #    curr_parity_data = parity_block_data
        
        #print "block data", block_data
        #updated_parity_data = curr_parity_data
        #print "parity data int ", updated_parity_data
        
        int_block_data = []
        for i in range(len(block_data)):
           int_block_data.append(ord(block_data[i]))
        for i in range(len(block_data), config.BLOCK_SIZE):
            int_block_data.append(0)
        
        int_parity_block_data = []
        for i in range(len(parity_block_data)):
           int_parity_block_data.append(ord(parity_block_data[i]))
        for i in range(len(parity_block_data), config.BLOCK_SIZE):
            int_parity_block_data.append(0)

        updated_parity_data = [0] * config.BLOCK_SIZE
        for i in range(config.BLOCK_SIZE):
            updated_parity_data[i] = int_parity_block_data[i] ^ int_block_data[i]
        
        new_updated_parity = updated_parity_data
        
        for i in range(config.BLOCK_SIZE):
            if updated_parity_data[i] != 0:
                new_updated_parity[i] = chr(updated_parity_data[i])
            else:
                new_updated_parity[i] = '\0'
                
        filesystem.update_data_block(parity_server_num, parity_blknum, ''.join(new_updated_parity))
        #print "parity data str ", new_updated_parity
        return ''.join(new_updated_parity)
    
    
    def update_parity(self, block_num, block_data):
        
        parity_server_num = config.NUM_OF_SERVERS - 1
        curr_parity = ''
        if block_num in self.parity_mapper:
            parity_block_num = self.parity_mapper[block_num]
            curr_parity = filesystem.get_data_block(parity_server_num, parity_block_num)
        return
    
    
    
    #REQUEST TO WRITE DATA ON THE THE SERVER
    def update_data_block(self, vblock_number, block_data):
        server1, block_num1 = self.get_server1_and_block_num(vblock_number)
        #server2, block_num2 = self.get_server2_and_block_num(vblock_number)
        #parity_server, parity_blknum = self.get_parity_server_and_block_num(vblock_number)
        
        #print "Write to Data Servers: ", server1, ", ", server2
        
        stime = config.SLEEP_TIME
        print "waiting ", stime, " seconds before first write"
        time.sleep(stime)
        
        print "Writing to server ", server1

        status = filesystem.update_data_block(server1, block_num1, block_data)
        self.update_parity(block_num1, block_data)
        if -1 == status:
            print ("Error VirtualBlockLayer: Server " + str(server1) + " not responding")

        parity_data = self.update_parity_data(block_num1, block_data)
        
        #--------------- print "waiting ", stime, " seconds before second write"
        #----------------------------------------------------- time.sleep(stime)
        #----------------------------------- print "Writing to server ", server2
        # status = filesystem.update_data_block(server2, block_num2, block_data)
        #------------------------------------------------------ if -1 == status:
            # print ("Error VirtualBlockLayer: Server " + str(server2) + " not responding")
#------------------------------------------------------------------------------ 
        #--------- parity_data = self.get_parity_data(vblock_number, block_data)
        # status = filesystem.update_data_block(parity_server, parity_blknum, parity_data)
        #-------------------------------- print filesystem.status(parity_server)
        #------------------------------------------------------ if -1 == status:
            # print ("Error VirtualBlockLayer: Server " + str(server2) + " not responding")
#------------------------------------------------------------------------------ 
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
        for server_number in range(self.numservers):
            status += str(server_number) + " : "
            status += filesystem.status(server_number)
        return status
    
    #REQUEST FOR THE STATUS OF FILE SYSTEM FROM SERVER
    def server_status(self, server_number):
        status = ""
        status += str(server_number) + " : "
        status += filesystem.status(server_number)
        return status


#------------------------------------------------------------ obj = Operations()
#------------------------------------------------ obj.Initialize_My_FileSystem()
#------------------------------------------------ b = obj.get_valid_data_block()
#----------------------------------------------------------- #obj.print_pnodes()
#-------------------------------------- obj.update_data_block(b, "hello world!")
#---------------------------------------------------- print obj.server_status(3)
#---------------------------------------------------- print obj.server_status(4)
#------------------------------------------------ c = obj.get_valid_data_block()
#----------------------------------------------------------- #obj.print_pnodes()
#------------------------------------- obj.update_data_block(c, "hello world!2")
#---------------------------------------------------- print obj.server_status(0)
#---------------------------------------------------- print obj.server_status(4)

#--------------------------------- obj.update_data_block(b, "hello wsdaf orld!")
#------------------------------ obj.update_data_block(b, "hellsadfasd o world!")
#-------------------------- obj.update_data_block(b, "hello wosdfasd as dfrld!")
#print obj.status()