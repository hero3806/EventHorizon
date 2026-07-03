from EventHorizon import Event
import callback

test_event = Event("Test")
test_event.Fire("Hey!")