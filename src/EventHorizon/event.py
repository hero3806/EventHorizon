from typing import Callable

class Event:
    _events = {}

    def __new__(cls, name):
        if name in cls._events:
            return cls._events[name]

        instance = super().__new__(cls)
        cls._events[name] = instance
        return instance

    def __init__(self, name):
        self.name = name
        if not hasattr(self, "callback"):
            self.callback = None
    
    def Fire(self, *args, **kwargs): 
        if not self.callback:
            raise Exception("There is no callback for this event, did you forget to add an 'OnEvent' callback?")
        
        self.callback(*args, **kwargs)
        
    def OnEvent(self, cb: Callable[..., None]):
        self.callback = cb
        return cb