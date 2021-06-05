class Notifier:
    def __init__(self):
        super().__init__()
        self.subs = []
    
    def subscribe(self, subscriber):
        self.subs.append(subscriber)
    
    def send_event(self, event_name='', event_data=None):
        print(f"sending event {event_name} with data: {event_data}")
        for s in self.subs:
            s.receive_event(event_name, event_data)
