from EventHorizon import Event

@Event("Test").OnEvent
def callback(message: str):
    print("Event recieved!!: ", message)