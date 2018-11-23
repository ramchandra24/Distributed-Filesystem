'''
THIS IS A MEMORY MODULE ON THE SREVER WHICH ACTS LIKE MEMORY OF FILE SYSTEM. ALL THE OPERATIONS REGARDING THE FILE SYSTEM OPERATES IN 
THIS MODULE. THE MODULE HAS POINTER TO DISK AND HAS EXACT SAME LAYOUT AS UNIX TYPE FILE SYSTEM.
'''  
import config, DiskLayout
from InodeOps import InodeOperations

#OPERATIONS ON FILE SYSTEM
class Operations():
	#POINTER TO DISK	
	def __init__(self):
		self.sblock = DiskLayout.SuperBlock()
		return
	
#BOOTS THE FILE SYSTEM
	def initialize(self):
		#ALLOCATING BITMAP BLOCKS 0 AND 1 BLOCKS ARE RESERVED FOR BOOT BLOCK AND SUPERBLOCK
		self.sblock.BITMAP_BLOCKS_OFFSET, count = 2, 2 
		for i in range(0, self.sblock.TOTAL_NO_OF_BLOCKS / self.sblock.BLOCK_SIZE):  	
			self.sblock.ADDR_BITMAP_BLOCKS.append(DiskLayout.Bitmap_Block(self.sblock.BLOCK_SIZE))
			count += 1
		#ALLOCATING INODE BLOCKS
		self.sblock.INODE_BLOCKS_OFFSET = count
		for i in range(0, (self.sblock.MAX_NUM_INODES * self.sblock.INODE_SIZE) / self.sblock.BLOCK_SIZE):		#for Inode blocks
			self.sblock.ADDR_INODE_BLOCKS.append(DiskLayout.Inode_Block(self.sblock.INODES_PER_BLOCK))
			count  += 1
		#ALLOCATING DATA BLOCKS
		self.sblock.DATA_BLOCKS_OFFSET = count
		for i in range(self.sblock.DATA_BLOCKS_OFFSET, self.sblock.TOTAL_NO_OF_BLOCKS):
			self.sblock.ADDR_DATA_BLOCKS.append(DiskLayout.Data_Block(self.sblock.BLOCK_SIZE))
		#MAKING BLOCKS BEFORE DATA BLOCKS UNAVAILABLE FOR USE SINCE OCCUPIED BY SUPERBLOCK, BOOTBLOCK, BITMAP AND INODE TABLE
		for i in range(0, self.sblock.DATA_BLOCKS_OFFSET): 
			self.sblock.ADDR_BITMAP_BLOCKS[i / self.sblock.BLOCK_SIZE].block[i % self.sblock.BLOCK_SIZE] = -1


	#GIVES ADDRESS OF INODE TABLE
	def addr_inode_table(self):
		return self.sblock.ADDR_INODE_BLOCKS


	#RETURNS THE DATA OF THE BLOCK
	def get_data_block(self, block_number):	
		if block_number == 0: print("Memory: Reserved for Boot Block")
		elif block_number == 1: print("Memory: Reserved for Super Block")
		elif block_number >= self.sblock.BITMAP_BLOCKS_OFFSET and block_number < self.sblock.INODE_BLOCKS_OFFSET:
			return self.sblock.ADDR_BITMAP_BLOCKS[block_number - self.sblock.BITMAP_BLOCKS_OFFSET].block
		elif block_number >= self.sblock.INODE_BLOCKS_OFFSET and block_number < self.sblock.DATA_BLOCKS_OFFSET:
			return self.sblock.ADDR_INODE_BLOCKS[block_number - self.sblock.INODE_BLOCKS_OFFSET].block
		elif block_number >= self.sblock.DATA_BLOCKS_OFFSET and block_number < self.sblock.TOTAL_NO_OF_BLOCKS:
			return self.sblock.ADDR_DATA_BLOCKS[block_number - self.sblock.DATA_BLOCKS_OFFSET].block
		else: print("Memory: Block index out of range or Wrong input!")
		return -1


	#RETURNS THE BLOCK NUMBER OF AVAIALBLE DATA BLOCK  
	def get_valid_data_block(self):			
		for i in range(0, self.sblock.TOTAL_NO_OF_BLOCKS):
			if self.sblock.ADDR_BITMAP_BLOCKS[i / self.sblock.BLOCK_SIZE].block[i % self.sblock.BLOCK_SIZE] == 0:
				self.sblock.ADDR_BITMAP_BLOCKS[i / self.sblock.BLOCK_SIZE].block[i % self.sblock.BLOCK_SIZE] = 1
				return i
		print("Memory: No valid blocks available")
		return -1

	#REMOVES THE INVALID DATA BLOCK TO MAKE IT REUSABLE
	def free_data_block(self, block_number):  	
		self.sblock.ADDR_BITMAP_BLOCKS[block_number / self.sblock.BLOCK_SIZE].block[block_number % self.sblock.BLOCK_SIZE] = 0
		b = self.sblock.ADDR_DATA_BLOCKS[block_number - self.sblock.DATA_BLOCKS_OFFSET].block
		for i in range(0, self.sblock.BLOCK_SIZE): b[i] = '\0'


	#WRITES TO THE DATA BLOCK
	def update_data_block(self, block_number, block_data):
		if block_number == -1:
			return
		b = self.sblock.ADDR_DATA_BLOCKS[block_number - self.sblock.DATA_BLOCKS_OFFSET].block
		for i in range(0, len(block_data)): b[i] = block_data[i]
		#print("Memory: Data Copy Completes")
	
	
	#UPDATES INODE TABLE WITH UPDATED INODE
	def update_inode_table(self, inode, inode_number):
		self.sblock.ADDR_INODE_BLOCKS[inode_number / self.sblock.INODES_PER_BLOCK].block[inode_number % self.sblock.INODES_PER_BLOCK] = inode

	
	#RETURNS THE INODE FROM INODE NUMBER
	def inode_number_to_inode(self, inode_number):
		return self.sblock.ADDR_INODE_BLOCKS[inode_number / self.sblock.INODES_PER_BLOCK].block[inode_number % self.sblock.INODES_PER_BLOCK]

	
	#SHOWS THE STATUS OF DISK LAYOUT IN MEMORY
	def status(self):
		counter = 1
		string = ""
		string += "\n----------BITMAP: ----------(Block Number : Valid Status)\n"
		block_number = 0
		for i in range(2, self.sblock.INODE_BLOCKS_OFFSET):
			string += "Bitmap Block : " + str(i - 2) + "\n"
			b = self.sblock.ADDR_BITMAP_BLOCKS[i - self.sblock.BITMAP_BLOCKS_OFFSET].block
			for j in range(0, len(b)):
				if j == 20: break   #only to avoid useless data to print
				string += "\t\t[" + str(block_number + j) + "  :  "  + str(b[j]) + "]  \n"
			block_number += len(b)
			if counter == 1: break
		string += ".....showing just part(20) of 1st bitmap block!\n"

		string += "\n\n----------INODE Blocks: ----------(Inode Number : Inode(Address)\n"
		inode_number = 0
		for i in range(self.sblock.INODE_BLOCKS_OFFSET, self.sblock.DATA_BLOCKS_OFFSET):
			string += "Inode Block : " + str(i - self.sblock.INODE_BLOCKS_OFFSET) + "\n"
			b = self.sblock.ADDR_INODE_BLOCKS[i - self.sblock.INODE_BLOCKS_OFFSET].block
			for j in range(0, len(b)):
				string += "\t\t[" + str(inode_number + j) + "  :  "  + str(bool(b[j])) + "]  \n"
			inode_number += len(b)
		
		string += "\n\n----------DATA Blocks: ----------\n  "
		counter = 0
		for i in range(self.sblock.DATA_BLOCKS_OFFSET, self.sblock.TOTAL_NO_OF_BLOCKS):
			if counter == 25: 
				string += "......Showing just part(25) data blocks\n"
				break
			string += (str(i) + " : " + "".join(self.sblock.ADDR_DATA_BLOCKS[i - self.sblock.DATA_BLOCKS_OFFSET].block)) + "  "
			counter += 1

		
		string += "\n\n----------HIERARCHY: ------------\n"
		for i in range(self.sblock.INODE_BLOCKS_OFFSET, self.sblock.DATA_BLOCKS_OFFSET):
			for j in range(0, self.sblock.INODES_PER_BLOCK):
				inode = self.sblock.ADDR_INODE_BLOCKS[i-self.sblock.INODE_BLOCKS_OFFSET].block[j]
				if inode and inode[0]:
					string += "\nDIRECTORY: " + inode[1] + "\n"
					for x in inode[7]: string += "".join(x[:config.MAX_FILE_NAME_SIZE]) + " || "
					string += "\n"
					#print inode
					#import InodeOps
					#tinode = InodeOps.InodeOperations().convert_array_to_table(inode)
					#tinode.print_file_metadata()
		
		return string
