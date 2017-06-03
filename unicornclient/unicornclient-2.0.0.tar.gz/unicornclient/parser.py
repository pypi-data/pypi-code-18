
class Parser(object):

    def __init__(self):
        self.buffer = ''
        self.state = 'start'
        self.size_to_read = 0

    def parse(self, data):
        self.buffer += data.decode()

        if self.state == 'start':
            if ':' in self.buffer:
                index = self.buffer.find(':')
                size = int(self.buffer[:index])
                #print("size: <" + str(size) + ">")
                self.size_to_read = size
                self.state = 'read'
                self.buffer = self.buffer[index+1:]

        if self.state == 'read':
            if len(self.buffer) >= self.size_to_read:
                payload = self.buffer[:self.size_to_read]
                #print("payload: <" + str(payload) + ">")
                self.state = 'start'
                self.buffer = self.buffer[self.size_to_read:]
                return payload

        return None
