import config

class RaidController():
    def __init__(self):
        self.file_counter = 0
        self.file_map_dict = {}
        return
    
    def file_locator(self, filename):
        if filename not in self.file_map_dict:
            first_server = self.file_counter
            second_server = (self.file_counter + 1) % config.NUM_OF_SERVERS
            self.file_map_dict[filename] = (first_server, second_server)
            self.file_counter = second_server
        return self.file_map_dict[filename]