from EventHorizon import Function

@Function("MyFunc").AttachFunction
def callback():
    return 67