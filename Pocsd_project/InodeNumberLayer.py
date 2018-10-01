'''
THIS MODULE ACTS AS A INODE NUMBER LAYER. NOT ONLY IT SHARES DATA WITH INODE LAYER, BUT ALSO IT CONNECTS WITH MEMORY INTERFACE FOR INODE TABLE 
UPDATES. THE INODE TABLE AND INODE NUMBER IS UPDATED IN THE FILE SYSTEM USING THIS LAYER
'''
import InodeLayer, config, MemoryInterface, datetime, InodeOps, MemoryInterface


#HANDLE OF INODE LAYER
interface = InodeLayer.InodeLayer()

class InodeNumberLayer():

	#PLEASE DO NOT MODIFY
	#ASKS FOR INODE FROM INODE NUMBER FROM MemoryInterface.(BLOCK LAYER HAS NOTHING TO DO WITH INODES SO SEPERTAE HANDLE)
	def INODE_NUMBER_TO_INODE(self, inode_number):
		array_inode = MemoryInterface.inode_number_to_inode(inode_number)
		inode = InodeOps.InodeOperations().convert_array_to_table(array_inode)
		if inode: inode.time_accessed = datetime.datetime.now()   #TIME OF ACCESS
		return inode


	#PLEASE DO NOT MODIFY
	#RETURNS DATA BLOCK FROM INODE NUMBER
	def INODE_NUMBER_TO_BLOCK(self, inode_number, offset, length):
		inode = self.INODE_NUMBER_TO_INODE(inode_number)
		if not inode:
			print("Error InodeNumberLayer: Wrong Inode Number! \n")
			return -1
		return interface.read(inode, offset, length)


	#PLEASE DO NOT MODIFY
	#UPDATES THE INODE TO THE INODE TABLE
	def update_inode_table(self, table_inode, inode_number):
		if table_inode: table_inode.time_modified = datetime.datetime.now()  #TIME OF MODIFICATION 
		array_inode = InodeOps.InodeOperations().convert_table_to_array(table_inode)
		MemoryInterface.update_inode_table(array_inode, inode_number)


	#PLEASE DO NOT MODIFY
	#FINDS NEW INODE INODE NUMBER FROM FILESYSTEM
	def new_inode_number(self, type, parent_inode_number, name):
		if parent_inode_number != -1:
			parent_inode = self.INODE_NUMBER_TO_INODE(parent_inode_number)
			if not parent_inode:
				print("Error InodeNumberLayer: Incorrect Parent Inode")
				return -1
			entry_size = config.MAX_FILE_NAME_SIZE + len(str(config.MAX_NUM_INODES))
			max_entries = (config.INODE_SIZE - 79 ) / entry_size
			if len(parent_inode.directory) == max_entries:
				print("Error InodeNumberLayer: Maximum inodes allowed per directory reached!")
				return -1
		for i in range(0, config.MAX_NUM_INODES):
			if self.INODE_NUMBER_TO_INODE(i) == False: #FALSE INDICTES UNOCCUPIED INODE ENTRY HENCE, FREEUMBER
				inode = interface.new_inode(type)
				inode.name = name
				self.update_inode_table(inode, i)
				return i
		print("Error InodeNumberLayer: All inode Numbers are occupied!\n")

	def is_file_in_dir(self, inode_number, parent_inode_number):
		if parent_inode_number != -1:
			parent_inode = self.INODE_NUMBER_TO_INODE(parent_inode_number)
			if not parent_inode:
				print("ERROR: InodeNumberLayer: Invalid directory")
				return False
			if inode_number not in parent_inode.directory:
				return False
		return True
	
	def is_file(self, inode_number):
		inode = self.INODE_NUMBER_TO_INODE(inode_number)
		if inode.type == 0:
			return True
		return False

	def is_dir(self, inode_number):
		inode = self.INODE_NUMBER_TO_INODE(inode_number)
		if inode.type == 1:
			return True
		return False


	#LINKS THE INODE
	def link(self, inode_number, parent_inode_number):
		'''WRITE YOUR CODE HERE'''
		inode = self.INODE_NUMBER_TO_INODE(inode_number)
		#Increment links made to the file
		parent_inode = self.INODE_NUMBER_TO_INODE(parent_inode_number)
		inode.links += 1
		#Update the inode in table
		self.update_inode_table(inode, inode_number)
		
		#self.update_inode_table(parent_inode, parent_inode_number)
		return


	#REMOVES THE INODE ENTRY FROM INODE TABLE
	def unlink(self, inode_number, parent_inode_number):
		'''WRITE YOUR CODE HERE'''
		inode = self.INODE_NUMBER_TO_INODE(inode_number)
		#If delete is called for directory, make links 0 and delete data blocks
		parent_inode = self.INODE_NUMBER_TO_INODE(parent_inode_number)
		#Decrement directory links by 2
		if self.is_dir(inode_number):
			if inode.links > 2:
				inode.links -= 1
			else:
				inode.links = 0
		#Decrement links made to the file
		else:	
			if inode.links > 0:
				inode.links -= 1
		#If there are no more links, delete the directory / file contents
		if inode.links == 0:
			print "No link to file/directory. Deleting the contents"
			#Free the memory occupied by inode
			interface.free_data_block(inode, 0)
			#Make the inode available for next files/directories
			self.update_inode_table(inode, 0)
		else:
			#Update the links to inode in table
			self.update_inode_table(inode, inode_number)
		return


	#IMPLEMENTS WRITE FUNCTIONALITY
	def write(self, inode_number, offset, data, parent_inode_number):
		'''WRITE YOUR CODE HERE'''
		inode = self.INODE_NUMBER_TO_INODE(inode_number)
		#Cannot write to a directory
		if self.is_dir(inode_number):
			print("Error InodeNumberLayer: Only files can be written!")
			return -1
		inode = interface.write(inode, offset, data)
		#Update file and directory inodes in table
		self.update_inode_table(inode, inode_number)
		parent_inode = self.INODE_NUMBER_TO_INODE(parent_inode_number)
		self.update_inode_table(parent_inode, parent_inode_number)
		return inode
		

	#IMPLEMENTS READ FUNCTIONALITY
	def read(self, inode_number, offset, length, parent_inode_number):
		'''WRITE YOUR CODE HERE'''
		inode = self.INODE_NUMBER_TO_INODE(inode_number)
		#Cannot read from a directory
		if self.is_dir(inode_number):
			print("Error InodeNumberLayer: Only files can be read!")
			return -1
		inode, data =  interface.read(inode, offset, length)
		#parent_inode = self.INODE_NUMBER_TO_INODE(parent_inode_number)

		#Update file inode in table
		self.update_inode_table(inode, inode_number)
		#Update directory modification time
		#self.update_inode_table(parent_inode, parent_inode_number)
		return data