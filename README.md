# Event Horizon

![PyPI Version](https://img.shields.io/pypi/v/ehorizon)
![Python Version](https://img.shields.io/pypi/pyversions/ehorizon)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-black?logo=github)](https://github.com/hero3806/EventHorizon)
![GitHub stars](https://img.shields.io/github/stars/hero3806/EventHorizon)
![GitHub license](https://img.shields.io/github/license/hero3806/EventHorizon)


[![PyPI Downloads](https://static.pepy.tech/personalized-badge/ehorizon?period=total&units=INTERNATIONAL_SYSTEM&left_color=BLACK&right_color=GREEN&left_text=downloads)](https://pepy.tech/projects/ehorizon)

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