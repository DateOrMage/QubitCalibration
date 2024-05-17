from nodes.BaseNode import BaseNode
from importlib import import_module

import matplotlib as plt

class NodesManager:
    """
    TODO class description ...
    """


    def __init__(self, nodes_names: list = [], current_node: str = None) -> None:
        """
        TODO Method description
        :param nodes_names: ...
        """
        self.current_node = current_node
        self.nodes_names = nodes_names


    def add_node(self, nodes) -> None:  # добавляем 1 или несколько узлов
        self.nodes_names.append(nodes)


    def remove_node(self, nodes) -> None:  # удаляем 1 или несколько узлов
        self.nodes_names.remove(nodes)


    def next_node(self) -> None:
        print(f'Current node is {self.current_node}')
        if self.current_node:
            curr_index = self.nodes_names.index(self.current_node)
        else:
            curr_index = -1
        if self.nodes_names[curr_index+1]:
            self.current_node = self.nodes_names[curr_index+1]


    def prev_node(self) -> None:
        print(f'Current node is {self.current_node}')
        if self.current_node:
            curr_index = self.nodes_names.index(self.current_node)
        else:
            curr_index = 0
        if self.nodes_names[curr_index-1]:
            self.current_node = self.nodes_names[curr_index-1]


    def execute_node(self, data_path: str = '') -> None:
        # TODO calculate node functionality
        curr_node_instance = getattr(import_module(f'nodes.{self.current_node}'), self.current_node)(data_path)
        x_max, plt = curr_node_instance.run()
        plt.show()
        print(f'Result {x_max} Mhz')
