class QuantizedSignal:
    def __init__(self):
        self.SignalType: bool = False
        self.IsPeriodic: bool = False  
        self.N1: int = 0
        self.data:list[tuple[int,int]]=[]
