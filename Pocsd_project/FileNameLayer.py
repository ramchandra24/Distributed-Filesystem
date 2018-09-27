'''
THIS MODULE ACTS LIKE FILE NAME LAYER AND PATH NAME LAYER (BOTH) ABOVE INODE LAYER.
IT RECIEVES INPUT AS PATH (WITHOUT INITIAL '/'). THE LAYER IMPLEMENTS LOOKUP TO FIND INODE NUMBER OF THE REQUIRED DIRECTORY.
PARENTS INODE NUMBER IS FIRST EXTRACTED BY LOOKUP AND THEN CHILD INODE NUMBER BY RESPECTED FUNCTION AND BOTH OF THEM ARE UPDATED
'''
import InodeNumberLayer

#HANDLE OF INODE NUMBER LAYER
interface = InodeNumberLayer.InodeNumberLayer()

class FileNameLayer():

	#PLEASE DO NOT MODIFY
	#RETURNS THE CHILD INODE NUMBER FROM THE PARENTS INODE NUMBER
	def CHILD_INODE_NUMBER_FROM_PARENT_INODE_NUMBER(self, childname, inode_number_of_parent):
		inode = interface.INODE_NUMBER_TO_INODE(inode_number_of_parent)
		if not inode: 
			print("Error FileNameLayer: Lookup Failure!")
			return -1
		if inode.type == 0:
			print("Error FileNameLayer: Invalid Directory!")
			return -1
		if childname in inode.directory: return inode.directory[childname]
		print("Error FileNameLayer: Lookup Failure!")
		return -1

	#PLEASE DO NOT MODIFY
	#RETUNS THE PARENT INODE NUMBER FROM THE PATH GIVEN FOR A FILE/DIRECTORY 
	def LOOKUP(self, path, inode_number_cwd):   
		name_array = path.split('/')
		if len(name_array) == 1: return inode_number_cwd
		else:
			child_inode_number = self.CHILD_INODE_NUMBER_FROM_PARENT_INODE_NUMBER(name_array[0], inode_number_cwd)
			if child_inode_number == -1: return -1
			return self.LOOKUP("/".join(name_array[1:]), child_inode_number)

	#PLEASE DO NOT MODIFY
	#MAKES NEW ENTRY OF INODE
	def new_entry(self, path, inode_number_cwd, type):
		if path == '/': #SPECIAL CASE OF INITIALIZING FILE SYSTEM
			interface.new_inode_number(type, inode_number_cwd, "root")
			return True
		parent_inode_number = self.LOOKUP(path, inode_number_cwd)
		parent_inode = interface.INODE_NUMBER_TO_INODE(parent_inode_number) 
		childname = path.split('/')[-1]
		if not parent_inode: return -1
		if childname in parent_inode.directory:
			print("Error FileNameLayer: File already exists!")
			return -1
		child_inode_number = interface.new_inode_number(type, parent_inode_number, childname)  #make new child
		if child_inode_number != -1:
			parent_inode.directory[childname] = child_inode_number
			interface.update_inode_table(parent_inode, parent_inode_number)


	#IMPLEMENTS READ
	def read(self, path, inode_number_cwd, offset, length):
		'''WRITE YOUR CODE HERE'''
		parent_inode_number = self.LOOKUP(path, inode_number_cwd)
		parent_inode = interface.INODE_NUMBER_TO_INODE(parent_inode_number) 
		childname = path.split('/')[-1]
		if not parent_inode: 
			print("Error FileNameLayer: Directory not found!")
			return -1
		if childname not in parent_inode.directory:
			print("Error: FileNameLayer: File not found in directory!")
			return -1
		inode_number = self.CHILD_INODE_NUMBER_FROM_PARENT_INODE_NUMBER(childname, parent_inode_number)
		return interface.read(inode_number, offset, length, parent_inode_number)


	#IMPLEMENTS WRITE
	def write(self, path, inode_number_cwd, offset, data):
		'''WRITE YOUR CODE HERE'''
		parent_inode_number = self.LOOKUP(path, inode_number_cwd)
		parent_inode = interface.INODE_NUMBER_TO_INODE(parent_inode_number) 
		childname = path.split('/')[-1]
		if not parent_inode: 
			print("Error FileNameLayer: Directory not found!")
			return -1
		if childname not in parent_inode.directory:
			print("Error: FileNameLayer: File not found in directory!")
			return -1
		inode_number = self.CHILD_INODE_NUMBER_FROM_PARENT_INODE_NUMBER(childname, parent_inode_number)
		return interface.write(inode_number, offset, data, parent_inode_number)
	
	
	#HARDLINK
	def link(self, old_path, new_path, inode_number_cwd):
		'''WRITE YOUR CODE HERE'''
		old_inode_number = self.LOOKUP(old_path, inode_number_cwd)
		new_inode_number = self.LOOKUP(new_path, inode_number_cwd)
		
		old_inode = interface.INODE_NUMBER_TO_INODE(old_inode_number)
		if False == interface.is_file(old_inode_number):
			print("Error FileNameLayer: Only files can be linked!")
			return -1
		if not old_inode:
			print("Error FileNameLayer: File to be linked not found!")
			return -1
		if False == interface.is_file(new_inode_number):
			print("Error FileNameLayer: Only files can be linked!")
			return -1
		new_inode = interface.INODE_NUMBER_TO_INODE(new_inode_number)
		if not new_inode:
			print("Error FileNameLayer: File to be linked to not found!")
			return -1
		return interface.link(old_inode_number, new_inode_number)
	
	
	#REMOVES THE FILE/DIRECTORY
	def unlink(self, path, inode_number_cwd):
		if path == "": 
			print("Error FileNameLayer: Cannot delete root directory!")
			return -1
		'''WRITE YOUR CODE HERE'''
		inode_number = self.LOOKUP(path, inode_number_cwd)
		return interface.unlink(inode_number, inode_number_cwd)



	#MOVE
	def mv(self, old_path, new_path, inode_number_cwd):
		
		'''WRITE YOUR CODE HERE'''
		old_inode_number = self.LOOKUP(old_path, inode_number_cwd)
		new_inode_number = self.LOOKUP(new_path, inode_number_cwd)
		if -1 != new_inode_number:
			print("Error FileNameLayer: File with new name already exists!")
			return -1
		
		old_inode = interface.INODE_NUMBER_TO_INODE(old_inode_number)
		if False == interface.is_file(old_inode_number):
			print("Error FileNameLayer: File not valid!")
			return -1
		if not old_inode:
			print("Error FileNameLayer: File to be moved not found!")
			return -1
		
		new_inode = interface.INODE_NUMBER_TO_INODE(new_inode_number)
		if not new_inode:
			print("Error FileNameLayer: Directory does not exist!")
			return -1
		if False == interface.is_dir(old_inode_number):
			print("Error FileNameLayer: Directory not valid!")
			return -1
		new_inode_number = self.new_entry(new_path, inode_number_cwd, old_inode.type)
		
		return interface.link(old_inode_number, new_inode_number)

	