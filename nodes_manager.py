from importlib import import_module
import logging
from operator import itemgetter

from NodeManagerErrors.NodeNameError import NodeNameError
from NodeManagerErrors.NoNextNodeError import NoNextNodeError
from NodeManagerErrors.NoPrevNodeError import NoPrevNodeError


lgr = logging.getLogger('QuantsLogger')
lgr.setLevel(logging.DEBUG)
fh = logging.FileHandler('log.txt')
fh.setLevel(logging.DEBUG)
frmt = logging.Formatter('%(asctime)s,%(name)s,%(levelname)s,%(message)s')
fh.setFormatter(frmt)
lgr.addHandler(fh)

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
                lgr.error(f'Thrown NodeNameError cause of incorrect values: {node_name}')
                raise NodeNameError(f'The list of nodes contains incorrect values: {node_name}')
                
        self.node_names.extend(nodes)
        lgr.info(f'Added nodes {nodes}')


    def clear_nodes(self):
        """ Method clears all nodes
            :return: None
        """
        self.node_names = []
        self.current_node = ''
        print('Nodes Cleared')

    def remove_nodes(self, *args) -> None:
        """ Method removes nodes from pipeline
            :param *args: tuple, int node indexes to remove
            :return: None
        """
        index_list = list(args)
        
        try:
            lgr.info(f'Removing nodes: {itemgetter(*index_list)(self.node_names)}')
            for i in sorted(index_list, reverse=True):
                self.node_names.remove(self.node_names[i])

            
        except IndexError:
            lgr.error(f'Thrown IndexError cause node with the specified index does not exist - {i}')
            raise IndexError(f'The node with the specified index does not exist - {i}')


    def set_default_nodes(self) -> None:
        """ Method sets default nodes to pipeline
            :return: None
        """
        self.add_nodes(self.default_nodes)
        lgr.info('Nodes set to default')

    def get_node_names(self):
        """ Method returns List of all pipeline nodes
            :return self.node_names: List of nodes
        """
        print('List of nodes:')
        for i in range(len(self.node_names)):
            print(f'[{i}] {self.node_names[i]}')
        return self.node_names

    def get_current_node(self) -> str:
        """ Method returns name of the current node
            :return: self.current_node: str, name of the current node
        """
        print(f'Current node is {self.current_node}')
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
            lgr.info(f'Moved forvard from {self.node_names[curr_index]} to {self.node_names[curr_index+1]}')
            print(f'Current node is {self.current_node}')
        except IndexError:
            lgr.error('Thrown NoNextNodeError cause next node is not exists')
            raise NoNextNodeError('There is no next node.')


    def prev_node(self) -> None:
        """ Method allows to move to the previous node
            :return: None
        """
        if self.current_node:
            curr_index = self.node_names.index(self.current_node)
        else:
            curr_index = 0
        if self.node_names[curr_index-1]:
            self.current_node = self.node_names[curr_index-1]
            lgr.info(f'Moved back from {self.node_names[curr_index]} to {self.node_names[curr_index-1]}')
            print(f'Current node is {self.current_node}')
        else:
            lgr.error(f'Thrown NoPrevNodeError cause previous node is not exists')
            raise NoPrevNodeError('There is no previous node.')
    
    def swap_nodes(self, index1, index2):
        """ Method allows to swap nodes
            :param index1: first index of node to swap
            :param index2: second index of node to swap
            :return: None
        """
        self.node_names[index1], self.node_names[index2] = self.node_names[index2], self.node_names[index1]

    def go_to_n(self, n) -> None:
        """ Method allows to go back n nodes
            :param n:
            :return: None
        """
        if self.current_node:
            curr_index = self.node_names.index(self.current_node)
        else:
            curr_index = 0
        if self.node_names[n]:
            self.current_node = self.node_names[n]
            print(f'Current node is {self.current_node}')
            lgr.info(f'Moved From {self.node_names[curr_index]} to {self.node_names[n]}')
        else:
            lgr.error(f'Thrown NoPrevNodeError cause previous node is not exists')
            raise NoPrevNodeError('There is no previous node.')
        

    def count_nodes(self):
        """ Method returns 
            :return self.node_names: List of nodes
        """
        return len(self.node_names)


    def execute_node(self, *args) -> None:
        """ Method Run calculations on the node and show the result
            :param data_path: str, path to pkl file for the current node
            :return: None
        """
        
        curr_node_instance = getattr(import_module(f'nodes.{self.current_node}'), self.current_node)()
        data = []
        data = curr_node_instance.run_measurements(*args)
        result, plot, is_correct = curr_node_instance.run(data)
        print(f'Result: {result}\nis_correct - {is_correct}')
        plot.show()
        lgr.info(f'Executed node is {self.current_node}. Results: {result}, Data correct flag: {is_correct}')

        return self.current_node, result, is_correct
        
