from overrides import override

from .BaseNode import BaseNode


class QubitSpectroscopyNode(BaseNode):

    def __init__(self, filename) -> None:
        super().__init__(filename)

    
    @override
    def convert_data(self):
        """ Method converts data to required type
            :return freq: np.ndarray, frequency data 
            :return SNRs: np.ndarray, SNRs data
        """
        pass
    
    
    @override
    def run():
        """ Method executing calculation on node
            :return result: str, str that represents specified value of frequency
            :return plt: plot, plot that shows optimized data
            :return is_correct: bool, flag indicating whether the data is correct 
        """
        pass
