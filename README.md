# Event Horizon

A python library that adds events to communicate through other files.

## Installation

```bash
pip install event-horizon
```

## Example Code Snippet

test.py:
```py
from EventHorizon import Event
import callback

myEvent = Event("MyEvent")

myEvent.Fire("Hello World!")
```

callback.py:
```py
from EventHorizon import Event

@Event("MyEvent").OnEvent
def callback(message):
    print(message)
```