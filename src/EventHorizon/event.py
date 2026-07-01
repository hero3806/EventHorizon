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
        if hasattr(self, "_initialized"):
            return

        self.name = name
        self.callback = None
        self._initialized = True
        
    @classmethod
    def delete_by_name(cls, name: str):
        """Deletes the function by the given name."""
        """@name Name of the function."""
        cls._events.pop(name, None)
    
    # Fires the event that has been binded from another file or the current file.
    # Supports multiple arguments.
    def Fire(self, *args, **kwargs): 
        """Fires the event that has been binded from another file or the current file."""
        """Supports multiple arguments."""
        if not self.callback:
            raise Exception("There is no callback for this event, did you forget to add an 'OnEvent' callback?")
        
        self.callback(*args, **kwargs)
    
    # Register the callback for the event
    def OnEvent(self, cb: Callable[..., None]):
        """Register the callback for the event"""
        self.callback = cb
        return cb
    
    def delete(self):
        """Delete the current event entirely"""
        """NOTE: Deleting this will make this instance completely unusable and will require creating a new instance."""
        Event._events.pop(self.name, None)