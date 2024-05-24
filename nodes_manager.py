from importlib import import_module

from NodeManagerErrors.NodeNameError import NodeNameError
from NodeManagerErrors.NoNextNodeError import NoNextNodeError
from NodeManagerErrors.NoPrevNodeError import NoPrevNodeError


class NodesManager:
    """ The NodesManager class is a Python class that manages a pipeline of nodes for running
        calculations. It allows adding, removing, and navigating through nodes in the pipeline. The
        class has methods for adding nodes, removing nodes, setting default nodes, getting the current
        node, moving to the next node, moving to the previous node, returning to a specific node, and
        executing the calculations on the current node.
    """
    
    default_nodes = [
            'ResonatorPeaksNode',
            'ResonatorSpectroscopyNode',
            'ScanningRangeDeterminationNode',
            'QubitSpectroscopyNode',
            'RawResonatorFreqCalNode',
            'RawQubitFreqCalNode',
            'RawQubitAmpCalNode',
            'AccurateResonatorFreqCalNode',
            'AccurateQubitAmpCalNode',
            'IQCalNode',
            'RamseyQubitFreqCalNode',
            'IQCalNode',
            'PreciselyQubitAmpCalNode',
            'IQCalNode',
            'QubitLifetimeNode',
            'IQCalNode',
        ]


    def __init__(self, node_names: list = [], current_node: str = '') -> None:
        """ Initialization class object.
            :param current_node: str, the pointer of the current node
            :param node_names: list[str], list of nodes for pipeline
            :return: None
        """
        self.current_node = current_node
        self.node_names = node_names

    def add_nodes(self, nodes) -> None:
        """ Method adds new nodes to pipeline
            :param nodes: list[str], list of nodes to add
            :return: None
        """
        for node_name in nodes:
            if node_name not in self.default_nodes:
                raise NodeNameError(f'The list of nodes contains incorrect values: {node_name}')
        self.node_names.extend(nodes)            


    def remove_nodes(self, indexes_str) -> None:
        """ Method removes nodes from pipeline
            :param indexes_str: str, str of node indexes to remove
            :return: None
        """
        index_list = [int(i) for i in indexes_str.split()]
        for i in sorted(index_list, reverse=True):
            try:
                self.node_names.remove(self.node_names[i])
            except IndexError:
                raise IndexError(f'The node with the specified index does not exist - {i}')


    def set_default_nodes(self) -> None:
        """ Method sets default nodes to pipeline
            :return: None
        """
        self.add_nodes(self.default_nodes)


    def get_current_node(self) -> str:
        """ Method returns name of the current node
            :return: self.current_node: str, name of the current node
        """
        return self.current_node
    

    def next_node(self) -> None:
        """ Method allows to move to the next node
            :return: None
        """
  
        if self.current_node:
            curr_index = self.node_names.index(self.current_node)
        else:
            curr_index = -1
        try:
            self.current_node = self.node_names[curr_index+1]
            print(f'Current node is {self.current_node}')
        except IndexError:
            raise NoNextNodeError('There is no next node.')


    def prev_node(self) -> None:
        """ Method allows to move to the previous node
            :return: None
        """
        print(f'Current node is {self.current_node}')
        if self.current_node:
            curr_index = self.node_names.index(self.current_node)
        else:
            curr_index = 0
        if self.node_names[curr_index-1]:
            self.current_node = self.node_names[curr_index-1]
        else:
            raise NoPrevNodeError('There is no previous node.')
    

    def return_to_n(self, n) -> None:
        """ Method allows to go back n nodes
            :param n:
            :return: None
        """
        print(f'Current node is {self.current_node}')
        if self.current_node:
            curr_index = self.node_names.index(self.current_node)
        else:
            curr_index = 0
        if self.node_names[curr_index-n]:
            self.current_node = self.node_names[curr_index-n]

    def execute_node(self, data_path: str = '') -> None:
        """ Method Run calculations on the node and show the result
            :param data_path: str, path to pkl file for the current node
            :return: None
        """
        curr_node_instance = getattr(import_module(f'nodes.{self.current_node}'), self.current_node)(data_path)
        x_max, plot, is_correct = curr_node_instance.run()
        
        plot.show()
        print(f'Result {x_max} Mhz\nis_correct - {is_correct}')
