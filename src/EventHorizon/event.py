from dataclasses import dataclass
from enum import Enum, auto
import threading
import warnings

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

class EventWarning(Warning):
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
        self._deleted = False
        
        self._waiters: list[tuple[threading.Event, dict[str, Any]]] = []
    
    def _ensure_valid(self):
        if self._deleted:
            raise EventError(
                f"Event {self.name!r} has been deleted and can no longer be used."
            )
        
    @classmethod
    def delete_by_name(cls, name: str):
        """
        Deletes the function by the given name.
        
        @name Name of the function.
        """
        cls._events.pop(name, None)
    
    # Fires the event that has been binded from another file or the current file.
    # Supports multiple arguments.
    def Fire(self, *args, **kwargs): 
        """
        Fires the event that has been binded from another file or the current file.
        
        Supports multiple arguments.
        """
        self._ensure_valid()
        
        for waiter, state in self._waiters.copy():
            state["args"] = args
            state["kwargs"] = kwargs
            waiter.set()
            
        if not self.callbacks:
            warnings.warn(
                "There are no callbacks for this event, did you forget to add an 'OnEvent' callback?",
                EventWarning,
                stacklevel=2
            )
            return
    
        for callback in self.callbacks.copy():
            
            if callback.type == EventType.EVENT:
                try:
                    callback.callback(*args, **kwargs)
                except Exception as e:
                    warnings.warn(
                        f"Callback {callback.callback.__name__!r} raised {type(e).__name__}: {e}",
                        EventWarning,
                        stacklevel=2,
                    )
                
            elif callback.type == EventType.ONCE:
                try:
                    callback.callback(*args, **kwargs)
                except Exception as e:
                    warnings.warn(
                        f"Callback {callback.callback.__name__!r} raised {type(e).__name__}: {e}",
                        EventWarning,
                        stacklevel=2,
                    )
                
                self.callbacks.remove(callback)
                
                
    
    # Register the callback for the event
    def OnEvent(self, cb: Callable[..., Any]):
        """Register a callback for the event"""
        
        self._ensure_valid()
        self.callbacks.append(Callback(cb))
        return cb
    
    def Once(self, cb: Callable[..., Any]):
        """Register a callback that runs only once."""
        
        self._ensure_valid()
        self.callbacks.append(Callback(cb, EventType.ONCE))
        return cb
    
    def Wait(self):
        """Block until the event fires."""
        
        self._ensure_valid()
        waiter = threading.Event()
        state: dict[str, Any] = {}

        self._waiters.append((waiter, state))

        try:
            waiter.wait()

            args = state["args"]
            kwargs = state["kwargs"]

            if kwargs:
                return args, kwargs

            if len(args) == 1:
                return args[0]

            return args
        finally:
            if (waiter, state) in self._waiters:
                self._waiters.remove((waiter, state))
    
    def delete(self):
        """
        Delete the current event entirely
        
        NOTE: Deleting this will make this instance completely unusable and will require creating a new instance.
        """
        if self._deleted:
            return

        Event._events.pop(self.name, None)
        self.callbacks.clear()
        self._waiters.clear()
        self._deleted = True
        
# Aliases
Event.fire = Event.Fire
Event.on = Event.OnEvent
Event.once = Event.Once
Event.wait = Event.Wait