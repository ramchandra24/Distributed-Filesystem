import MemoryInterface, AbsolutePathNameLayer
import FileNameLayer
import time

def Initialize_My_FileSystem():
    MemoryInterface.Initialize_My_FileSystem()
    AbsolutePathNameLayer.AbsolutePathNameLayer().new_entry('/', 1)

#HANDLE TO ABSOLUTE PATH NAME LAYER
interface = AbsolutePathNameLayer.AbsolutePathNameLayer()

class FileSystemOperations():

    #MAKES NEW DIRECTORY
    def mkdir(self, path):
        start_time = time.time()
        interface.new_entry(path, 1)
        print "Time to make a directory ", (time.time() - start_time)

    #CREATE FILE
    def create(self, path):
        start_time = time.time()
        interface.new_entry(path, 0)
        print "Time to create file ", (time.time() - start_time)
        

    #WRITE TO FILE
    def write(self, path, data, offset=0):
        start_time = time.time()
        interface.write(path, offset, data)
        print "Time to write to a file ", (time.time() - start_time)
      

    #READ
    def read(self, path, offset=0, size=-1):
        start_time = time.time()
        read_buffer = interface.read(path, offset, size)
        if read_buffer != -1: print(path + " : " + read_buffer)
        print "Time to read file ", (time.time() - start_time)

    
    #DELETE
    def rm(self, path):
        start_time = time.time()
        interface.unlink(path)
        print "Time to remove file/folder  ", (time.time() - start_time)


    #MOVING FILE
    def mv(self, old_path, new_path):
        start_time = time.time()
        interface.mv(old_path, new_path)
        print "Time to move file/folder ", (time.time() - start_time)

    def link(self, old_path, new_path):
        start_time = time.time()
        interface.link(old_path, new_path)
        print "Time to create link ", (time.time() - start_time)
        
    #CHECK STATUS
    def status(self):
        print(MemoryInterface.status())
        #print(FileNameLayer.status())


if __name__ == '__main__':
    #DO NOT MODIFY THIS
    Initialize_My_FileSystem()
    my_object = FileSystemOperations()
    #my_object.status()
    #YOU MAY WRITE YOUR CODE AFTER HERE

    my_object.mkdir("/A")
    my_object.create("/A/1.txt")
    my_object.create("/A/2.txt")
    #my_object.create("/A/2.txt")
    my_object.write("/A/1.txt", "Lorerm asdlkfj sdf", 0)
    my_object.write("/A/1.txt", "Lorerm asdlkfj sdf", 10)
    my_object.write("/A/1.txt", "Lorerm asdlkfj sdf", 20)
    my_object.write("/A/2.txt", "Lorer2dfm asdlkfj sdf", 0)
    #print "writing second chunk"
    #my_object.write("/A/1.txt", "Autodidacticism is sometimes", 10)
    #my_object.write("/A/1.txt", "Autodidacticism is sometimes", 13)

    #print "writing third chunk"
    ##my_object.write("/A/1.txt", "test data cut here", 20)
    ##my_object.write("/A/1.txt", "Autoometimes", 16)
    #print "writing fourth chunk"    
    #my_object.write("/A/1.txt", "Autodidacticism is sometimes", 23)
    #my_object.write("/A/1.txt", "test data cut here", 35)
    ##my_object.write("/A/1.txt", "Autodidacticism is sometimes", 30)
    #my_object.write("/A/1.txt", "Autodidacticism is sometimes", 43)
    #my_object.write("/A/2.txt", "Autodidacticism is sometimes", 0)
    #my_object.write("/A/2.txt", "Autodidacticism is sometimes", 0)
    #my_object.status()
    #my_object.mkdir("/A/C")
    #my_object.mkdir("/B/D")

    #my_object.mkdir("/A/C/E")
    #my_object.mkdir("/B/D/F")

    #my_object.mkdir("/A/C/E/G")
    #my_object.mkdir("/B/D/F/H")

    #my_object.mkdir("/I")
    #my_object.mkdir("/J")

    #my_object.mkdir("/K")
    #my_object.mkdir("/L")
    
    #--------------------------------------------------- my_object.mkdir("/I/M")
    #--------------------------------------------------- my_object.mkdir("/J/N")
#------------------------------------------------------------------------------ 
    #--------------------------------------------------- my_object.mkdir("/K/O")
    #--------------------------------------------------- my_object.mkdir("/L/P")
#------------------------------------------------------------------------------ 
    #------------------------------------------------- my_object.mkdir("/I/M/Q")
    #------------------------------------------------- my_object.mkdir("/J/N/R")
#------------------------------------------------------------------------------ 
    #------------------------------------------------- my_object.mkdir("/K/O/S")
    #------------------------------------------------- my_object.mkdir("/L/P/T")
#------------------------------------------------------------------------------ 
    #----------------------------------------------- my_object.mkdir("/I/M/Q/U")
    #----------------------------------------------- my_object.mkdir("/J/N/R/V")
#------------------------------------------------------------------------------ 
    #----------------------------------------------- my_object.mkdir("/K/O/S/W")
    #----------------------------------------------- my_object.mkdir("/L/P/T/X")
#------------------------------------------------------------------------------ 
    #--------------------------------------------- my_object.mkdir("/I/M/Q/U/Y")
    #--------------------------------------------- my_object.mkdir("/J/N/R/V/Z")
    
    #my_object.create("/A/1.txt")
    #my_object.create("/2.txt")
    #my_object.mkdir("/A/C")
    #my_object.link("/", "/A/C/4.txt")
    #my_object.link("/A/C/4.txt", "/A/C/5.txt")
    #my_object.status()
    #my_object.rm("/A/C/5.txt")
    #my_object.status()
    #my_object.mkdir("/A/C/B")
    #my_object.create("/A/C/1.txt")
    #my_object.write("/A/1.txt", "test data cut here", 0)
    #my_object.write("/A/1.txt", "Autodidacticism is sometimes", 10)
    #my_object.write("/A/1.txt", "Autodidacticism is sometimes", 13)
    #my_object.link("/A/1.txt", "/A/2.txt")
    #my_object.read("/A/1.txt", 0, 100)
    #my_object.status()
    #my_object.link("/A/1.txt", "/B/2.txt")
    #my_object.link("/A/1.txt", "/A/C/2.txt")
    #my_object.mkdir("/A/D")
    #my_object.status()
    #my_object.mv("/2.txt", "/A/1.txt") #File name in to dir. INVALID
    #my_object.mv("/2.txt", "/A/C/B/")
    #my_object.link("/A/C/B", "/A/C/B/3.txt")
    #my_object.link("/A/C/B/3.txt", "/")
    #my_object.mv("/A/C", "/")
    #my_object.mkdir("/D")
    #my_object.rm("/D")
    #my_object.write("/A/C/2.txt", "directory c write", 6)
    #my_object.rm("/A/1.txt")
    #my_object.status()
    #my_object.rm("/A/C/1.txt")
    #my_object.status()
    #my_object.rm("/B/2.txt")
    #my_object.rm("/B")
    #my_object.rm("/A")
    
    '''Examples:
    my_object.mkdir("/A")
    my_object.status()
    my_object.mkdir("/B")
    my_object.status()
    my_object.create("/A/1.txt"), as A is already there we can crete file in A
    my_object.status()
    my_object.write("A/1.txt", "POCSD", offset), as 1.txt is already created now, we can write to it.
    my_object.status()
    my_object.mv("/A/1.txt", "/B")
    my_object.status()
    my_object.rm("A/1.txt")
    my_object.status()
    '''

