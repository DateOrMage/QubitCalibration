

class NodesManager:
    """
    TODO class description ...
    """
    __name_current_node: str = None

    def __init__(self, nodes_names: list = None) -> None:
        """
        TODO Method description
        :param nodes_names: ...
        """
        self.nodes_names = nodes_names

    def add_node(self) -> None:  # добавляем 1 или несколько узлов
        pass

    def remove_node(self) -> None:  # удаляем 1 или несколько узлов
        pass

    def next_node(self) -> None:
        print(f'Current node is {self.__name_current_node}')
        pass

    def prev_node(self) -> None:
        print(f'Current node is {self.__name_current_node}')
        pass

    def execute_node(self, data_path: str) -> None:
        # TODO calculate node functionality
        print(f'Result ...')
        pass
