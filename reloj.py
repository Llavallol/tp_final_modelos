from notifier import Notifier

class Reloj:
    def __init__(self):
        super().__init__()
        self.time = 0
    
    def get_time(self):
        return self.time
    
    def advance(self):
        self.time += 1
        