from EventHorizon import Event

@Event("Test").OnEvent
def callback(message: str):
    print("Event recieved!!: ", message)
    
@Event("Test").OnEvent
def callback2(message: str):
    print("this has been recieved too", message)