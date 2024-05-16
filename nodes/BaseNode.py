import numpy as np
import pickle
from abc import ABC, abstractmethod


class BaseNode(ABC):
    def __init__(self, filename) -> None:
        self.filename = filename


    def get_data(self):
        with open(self.filename, 'rb') as file:
            data = pickle.load(file)
            return data


    def entropy_H1_new(y, n_intervals=10):
        '''Энтропия H1'''
    
        intervals = np.linspace(y.min(), y.max(), n_intervals+1)
        counts, _ = np.histogram(y, bins=intervals)
        N = len(y)
        p = counts / N
        p = p[p != 0]
        entropy = -np.sum(p * np.log2(p))
        return entropy


    def entropy_H2(y, n_intervals=10):
        '''Энтропия H2'''
        y_min, y_max = np.min(y), np.max(y)
        interval_size = (y_max - y_min) / n_intervals
        N = len(y)
        p = []
        for i in range(n_intervals):
            interval_start = y_min + i * interval_size
            interval_end = interval_start + interval_size
            interval_count = np.sum((y >= interval_start) & (y < interval_end))
            p_interval = interval_count / N
            p.append(p_interval)
        p = np.array(p)
        p = p[p != 0]
        entropy = -np.sum(p * np.log2(p))
        return entropy

    def entropy_H3(y):
        '''Энтропия H3'''
        # индексы сортированных значений, чтобы увидеть значения в порядке возрастания
        sorted_indices = np.argsort(y)
        # подсчет числа случаев для каждой перестановки
        N = len(y)
        counts = np.zeros((N, N, N))
        for i in range(N - 2):
            perm = sorted_indices[i:i + 3]
            if all(perm[j] < perm[j + 1] for j in range(2)):
                counts[tuple(perm)] += 1
        flattened_counts = counts.flatten() # в одномерный массив перевод
        p = flattened_counts / (N - 2)
        p = p[p != 0] #чтоб не было деления на ноль
        entropy = -np.sum(p * np.log2(p))
        return entropy


    @abstractmethod
    def convert_data(self):
        pass


    @abstractmethod
    def run() -> np.ndarray:
        pass