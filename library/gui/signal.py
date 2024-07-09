class Signal:
    def __init__(self):
        self.connections: list[callable] = []
    
    def connect(self, connection: callable):
        self.connections.append(connection)
    
    def disconnect(self, connection: callable):
        try:
            self.connections.remove(connection)
        except:
            pass
    
    def emit(self, *args, **kwargs):
        for connection in self.connections:
            connection(*args, **kwargs)
