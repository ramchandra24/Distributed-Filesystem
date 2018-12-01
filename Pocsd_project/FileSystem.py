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

    my_object.mkdir("/A")
    my_object.create("/A/1.txt")
    my_object.write("/A/1.txt", "Autodidacticism is sometimes", 10)
    #my_object.create("/2.txt")
    my_object.link("/A/1.txt", "/2.txt")
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


