from nodes.BaseNode import BaseNode
from importlib import import_module

import matplotlib as plt

from NodeManagerErrors.NodeNameError import NodeNameError
from NodeManagerErrors.NoNextNodeError import NoNextNodeError
from NodeManagerErrors.NoPrevNodeError import NoPrevNodeError

class NodesManager:
    """
    TODO class description ...
    """


    default_nodes = [
            ('ResonatorPeaksNode', 1),
            ('ResonatorSpectroscopyNode', 1),
            ('ScanningRangeDeterminationNode', 1),
            ('QubitSpectroscopyNode', 1),
            ('RawResonatorFreqCalNode', 1),
            ('RawQubitFreqCalNode', 1),
            ('RawQubitAmpCalNode', 1),
            ('AccurateResonatorFreqCalNode', 1),
            ('AccurateQubitAmpCalNode', 1),
            ('IQCalNode', 1),
            ('RamseyQubitFreqCalNode', 1),
            ('IQCalNode', 1),
            ('PreciselyQubitAmpCalNode', 1),
            ('IQCalNode', 1),
            ('QubitLifetimeNode', 1),
            ('IQCalNode', 1),
        ]
    default_node_names = [node_name for node_name, _ in default_nodes]


    def __init__(self, node_names: list = [], current_node: tuple = None) -> None:
        """
        TODO Method description
        :param node_names: ...
        """
        self.current_node = current_node
        self.node_names = node_names
        self.curr_node_steps_back = None

    def add_nodes(self, nodes) -> None:
        '''Добавляем 1 или несколько узлов'''
        for node_name, steps_back in nodes:
            if node_name not in self.default_node_names or steps_back < 0:
                raise NodeNameError('Список узлов содержит некорректные значения. ', node_name)
        self.node_names.extend(nodes)            


    def remove_nodes(self, nodes) -> None:
        '''Удаляем 1 или несколько узлов'''
        for node in self.node_names:
            try:
                if node[0] in nodes:
                    self.node_names.remove(node)
            except NodeNameError:
                raise NodeNameError('Указанного узла нет в списке. ', node)

    def set_default_nodes(self):
        '''Установить узлы по умолчанию'''
        self.add_nodes(self.default_nodes)


    def next_node(self) -> None:
        '''Перейти к следующему узлу'''
        print(f'Current node is {self.current_node}')
        if self.current_node:
            curr_index = self.node_names.index((self.current_node, self.curr_node_steps_back))
        else:
            curr_index = -1
        try:
            self.current_node = self.node_names[curr_index+1][0]
            self.curr_node_steps_back = self.node_names[curr_index+1][1]
        except IndexError:
            raise NoNextNodeError('Следующего узла не существует.')


    def prev_node(self) -> None:
        '''Перейти к предыдущему узлу'''
        print(f'Current node is {self.current_node}')
        if self.current_node:
            curr_index = self.node_names.index((self.current_node, self.curr_node_steps_back))
        else:
            curr_index = 0
        if self.node_names[curr_index-1]:
            self.current_node = self.node_names[curr_index-1][0]
            self.curr_node_steps_back = self.node_names[curr_index-1][1]
        else:
            raise NoPrevNodeError('Предыдущего узла не существует.')
    

    def retutn_to_n(self):
        '''Вернутся к необходимому узлу после неудачной калибровки'''
        print(f'Current node is {self.current_node}')
        if self.current_node:
            curr_index = self.node_names.index(self.current_node)
        else:
            curr_index = 0
        if self.node_names[curr_index-self.curr_node_steps_back]:
            self.current_node = self.node_names[curr_index-self.curr_node_steps_back]

    def execute_node(self, data_path: str = '') -> None:
        '''Запустить вычисления на узле'''
        # TODO calculate node functionality
        curr_node_instance = getattr(import_module(f'nodes.{self.current_node}'), self.current_node)(data_path)
        x_max, plt, is_correct = curr_node_instance.run()
        
        plt.show()
        print(f'Result {x_max} Mhz\nis_correct - {is_correct}')
