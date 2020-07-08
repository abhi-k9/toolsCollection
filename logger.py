
# TODO : Write docstring neatly
class debug_logger:
    """Replace 'if log then log' statements with succinct single statement. Also allows switching debug on/off in middle"""
    
    def log(message):
    """Print debugging messages to terminal (despite any redefinition of stdout by the program)"""
    sys.__stdout__.write(message)
    
    def __init__(self, debug_bool):
        self.debug_on = debug_bool
    
    def set_debug_mode(self, debug_bool):
        self.debug_on = debug_bool
        
    def debug_mode(self):
        return self.debug_on    
        
    def __call__(self, message):
        if self.debug_on:
            log(message)