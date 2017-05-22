from logging import Filter

class Location(Filter):
    
    def __init__(self, filename=None, lineno=None, pathname=None):
        
        self.filename = filename
        self.lineno = lineno
        self.pathname = pathname
        
        if not lineno:
            return
        
        if type(lineno) is type([]):
            self.lineno = list(range(lineno[0]+1, lineno[1]+1))
        
    
    def filter(self, record):
        
        if all([self.filename is None, self.lineno is None, self.pathname is None]):
            return True
        
        output = False
        
        if record.filename == self.filename:
            output = True
        
        if record.pathname == self.pathname:     
            output = True
            
        if not self.lineno:
            return output
        
        output = False
            
        if type(self.lineno) is type([]) and record.lineno in self.lineno:
            output = True
        elif self.lineno == record.lineno:
            output = True
            
        return output
        
            
        