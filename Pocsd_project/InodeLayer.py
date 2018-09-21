'''
THIS MODULE IS INODE LAYER OF THE FILE SYSTEM. IT INCLUDES THE INODE DEFINITION DECLARATION AND GLOBAL HANDLE OF BLOCK LAYER OF API.
THIS MODULE IS RESPONSIBLE FOR PROVIDING ACTUAL BLOCK NUMBERS SAVED IN INODE ARRAY OF BLOCK NUMBERS TO FETCH DATA FROM BLOCK LAYER.
'''
import datetime, config, BlockLayer, InodeOps

#HANDLE OF BLOCK LAYER
interface = BlockLayer.BlockLayer()

class InodeLayer():

    #RETURNS BLOCK NUMBER FROM RESPECTIVE INODE DIRECTORY
    def INDEX_TO_BLOCK_NUMBER(self, inode, index):
        if index == len(inode.blk_numbers): return -1
        return inode.blk_numbers[index]


    #RETURNS BLOCK DATA FROM INODE
    def INODE_TO_BLOCK(self, inode, offset):
        index = offset / config.BLOCK_SIZE
        block_number = self.INDEX_TO_BLOCK_NUMBER(inode, index)
        if block_number == -1: return ''
        else: return interface.BLOCK_NUMBER_TO_DATA_BLOCK(block_number)


    #MAKES NEW INODE OBJECT
    def new_inode(self, type):
        return InodeOps.Table_Inode(type)


    #FLUSHES ALL THE BLOCKS OF INODES FROM GIVEN INDEX OF MAPPING ARRAY  
    def free_data_block(self, inode, index):
        for i in range(index, len(inode.blk_numbers)):
            interface.free_data_block(inode.blk_numbers[i])
            inode.blk_numbers[i] = -1


    #IMPLEMENTS WRITE FUNCTIONALITY
    def write(self, inode, offset, data):
        index = offset / config.BLOCK_SIZE         
        last_blk_index = self.INDEX_TO_BLOCK_NUMBER(inode, index)  #FETCHING COMPLETE BLOCK OF GIVEN OFFSET
        
        if last_blk_index == -1: last_blk_index = 0     #IF -1, MEANS DATA IS FRESHLY WRITTEN
        inode, prev_data = self.read(inode, offset - (offset % config.BLOCK_SIZE), offset % config.BLOCK_SIZE)  #TRIMMING DATA ACCORDING TO OFFSET
        if prev_data == -1:         #IF GIVEN OFFSET EXCEEDS THE FILE LENGTH
            print("Error(write) InodeLayer: Offset exceeds the file length")
            return inode
        data = prev_data[: offset % config.BLOCK_SIZE] + data 
        self.free_data_block(inode, index)  #INVALIDIATING ALL BLOCKS INCLUDING AND AFTER OFFSET BLOCK
        
        inode.size = (index * config.BLOCK_SIZE) + len(data) + 1 if last_blk_index != 0 else len(data) + 1#UPDATING SIZE
        blocks = [data[i:i+config.BLOCK_SIZE] for i in range(0, len(data), config.BLOCK_SIZE)] #BREAKING DATA IN BLOCKS
        total_blocks = len(blocks)#check if total data exceeds required length
        
        if total_blocks > len(inode.blk_numbers):  #IF DATA EXCEEDS THE MAXIMUM ALLOCATED SIZE
            print("Error InodeLayer: Data exceeds the given size. Incomplete write!")
            total_blocks = len(inode.blk_numbers)
            inode.size = total_blocks * config.BLOCK_SIZE  #UPDATING SIZE 
        
        for i in range(0, total_blocks):     #WRITING BLOCKS
            new_valid_block_number = interface.get_valid_data_block()
            inode.blk_numbers[i] = new_valid_block_number
            interface.update_data_block(new_valid_block_number, blocks[i])

        inode.time_accessed = datetime.datetime.now()
        inode.time_modified = datetime.datetime.now() 
        return inode  #RETURNS INODE TO INODE NUMBER LAYER TO UPDATE INODE AT SERVER
       

    #IMPLEMENTS THE READ FUNCTION 
    def read(self, inode, offset, length): 
        if type == 1: 
            print("Error InodeLayer: Wrong Inode for file read")
            return -1
        if offset >= inode.size + 1: 
            print("Error(Read) InodeLayer: Offset exceeds the file length")
            return inode, -1
            #offset = 0
        if length >= inode.size + 1:
            print("Error(Read) InodeLayer: Length exceeds the file length")
            return inode, -1
            #length = inode.size - offset
        if length == 0: 
            return inode, ""
        if length == -1: 
            length = inode.size -1
        
        curr_offset  = offset 
        end_offset = (offset + length) +  (config.BLOCK_SIZE - ((offset + length) % config.BLOCK_SIZE))
        data = ''
        
        while curr_offset <= end_offset:
            data += self.INODE_TO_BLOCK(inode, curr_offset)
            curr_offset += config.BLOCK_SIZE
        
        start = offset % config.BLOCK_SIZE
        end = start + length   
        inode.time_accessed = datetime.datetime.now()
        return inode, data[start : end]                               #RETURNS INODE TO INODE NUMBER LAYER TO UPDATE INODE AT SERVER



