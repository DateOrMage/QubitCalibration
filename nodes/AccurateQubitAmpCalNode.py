from overrides import override
from BaseNode import BaseNode


class AccurateQubitAmpCalNode(BaseNode):
    '''Точная калибровка амплитуды кубита'''
    def __init__(self, filename) -> None:
        super().__init__(filename)

    
    @override
    def convert_data(self):
        pass
    
    
    @override
    def run(self):
        pass