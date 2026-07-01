# Event Horizon

A python library that adds events to communicate through other files.

## Installation

```bash
pip install ehorizon
```

## Example Code Snippet

- Events:

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

- Functions:

test.py:
```py
from EventHorizon import Function
import function

myFunc = Function("MyFunc")

favourite_number = myFunc.run()

print(favourite_number)
```

function.py:
```py
from EventHorizon import Function

@Function("MyFunc").AttachFunction
def callback():
    return 5
```