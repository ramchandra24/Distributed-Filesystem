# Mapping functionalities
import config
import time
import MemoryInterface_RPC as Memory
filesystem = Memory.Operations()
numservers = config.NUM_OF_SERVERS
#HANDLE FOR MEMORY OPERATIONS
class Operations():
	def __init__(self, type):
		self.bigdict = {}
		self.client_blknum_counter = 0
	
	#REQUEST TO BOOT THE FILE SYSTEM
	def Initialize_My_FileSystem(self):
		print("File System Initializing......")
		time.sleep(2)
		Memory.Initialize()
		print("File System Initialized!")


	#REQUEST TO FETCH THE INODE FROM INODE NUMBER FROM SERVER
	def inode_number_to_inode(self, inode_number):
		return filesystem.inode_number_to_inode(inode_number)


	#REQUEST THE DATA FROM THE SERVER
	def get_data_block(self, block_number):
		for server,server_blknum in bigdict[block_number].items():
			try:
				return ''.join(filesystem.get_data_block(block_number))
			except Exception as error:
				print "server: " + server + " is not working"


	#REQUESTS THE VALID BLOCK NUMBER FROM THE SERVER 
	def get_valid_data_block(self):
		smalldict = {}
		server_offset = self.client_blknum_counter % numservers
		serverA = server_offset
		serverB = server_offset + 1
		serverA_blknum = filesystem.get_valid_data_block(serverA)
		serverB_blknum = filesystem.get_valid_data_block(serverB)
		smalldict[serverA] = serverA_blknum
		smalldict[serverB] = serverB_blknum
		self.bigdict[client_blknum_counter] = smalldict
		self.client_blknum_counter = self.client_blknum_counter + 1
		return client_blknum_counter


	#REQUEST TO MAKE BLOCKS RESUABLE AGAIN FROM SERVER
	def free_data_block(self, block_number):
		for server,server_blknum in bigdict[block_number].items():
			filesystem.free_data_block(server, server_blknum)


	#REQUEST TO WRITE DATA ON THE THE SERVER
	def update_data_block(self, block_number, block_data):
		for server,server_blknum in bigdict[block_number].items():
			filesystem.update_data_block(server, server_blknum, block_data)


	#REQUEST TO UPDATE THE UPDATED INODE IN THE INODE TABLE FROM SERVER
	def update_inode_table(self, inode, inode_number):
		filesystem.update_inode_table(inode, inode_number)


	#REQUEST FOR THE STATUS OF FILE SYSTEM FROM SERVER
	def status(self):
		return filesystem.status()

	