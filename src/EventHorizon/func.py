from typing import Callable
from typing import Any

class Function:
    _funcs = {}
    
    def __new__(cls, name):
        if name in cls._funcs:
            return cls._funcs[name]

        instance = super().__new__(cls)
        cls._funcs[name] = instance
        return instance

    def __init__(self, name):
        self.name = name
        if not hasattr(self, "callback"):
            self.callback = None
            
    def run(self, *args, **kwargs): 
        """Fires the function that has been binded and returns the value from it."""
        """Supports multiple arguments."""
        if not self.callback:
            raise Exception("There is no callback for this function, did you forget to add an 'AttachFunction' callback?")
        
        return self.callback(*args, **kwargs)
        
    def AttachFunction(self, cb: Callable[..., Any]):
        """Register the callback for the function"""
        self.callback = cb
        return cb