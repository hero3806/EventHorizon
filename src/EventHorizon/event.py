from dataclasses import dataclass
from enum import Enum, auto
import threading
from typing import Any, Callable

class EventType(Enum):
    EVENT = auto()
    WAIT = auto()
    ONCE = auto()
    
@dataclass(slots=True, frozen=True)
class Callback:
    callback: Callable[..., Any]
    type: EventType = EventType.EVENT

class EventError(Exception):
    pass

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
        self.callbacks: list[Callback] = []
        self._initialized = True
        
        self._waiter = threading.Event()
        self._wait_args = ()
        self._wait_kwargs = {}
    
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
        if not self.callbacks:
            raise EventError("There are no callbacks for this event, did you forget to add an 'OnEvent' callback?")
        
        self._wait_args = args
        self._wait_kwargs = kwargs
        self._waiter.set()
    
        for callback in self.callbacks.copy():
            
            if callback.type == EventType.EVENT:
                callback.callback(*args, **kwargs)
            elif callback.type == EventType.ONCE:
                callback.callback(*args, **kwargs)
                self.callbacks.remove(callback)
                
                
    
    # Register the callback for the event
    def OnEvent(self, cb: Callable[..., None]):
        """Register a callback for the event"""
        
        self.callbacks.append(Callback(cb))
        return cb
    
    def Once(self, cb: Callable[..., None]):
        """Register a callback that runs only once."""
        
        self.callbacks.append(Callback(cb, EventType.ONCE))
        return cb
    
    def Wait(self):
        """Block until the event fires."""

        self._waiter.wait()

        args = self._wait_args
        kwargs = self._wait_kwargs

        self._waiter.clear()

        if kwargs:
            return args, kwargs

        if len(args) == 1:
            return args[0]

        return args
        
    def delete(self):
        """Delete the current event entirely"""
        """NOTE: Deleting this will make this instance completely unusable and will require creating a new instance."""
        Event._events.pop(self.name, None)
        
# Aliases
Event.fire = Event.Fire
Event.on = Event.OnEvent
Event.once = Event.Once
Event.wait = Event.Wait