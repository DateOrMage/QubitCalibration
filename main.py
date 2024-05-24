from nodes_manager import NodesManager

test = NodesManager()
test.add_nodes(['RawQubitAmpCalNode', 'AccurateResonatorFreqCalNode', ])
for i, node in enumerate(test.node_names):
    print(f'{i}: {node}')
test.remove_nodes(input('Введите индексы для удаления'))
for i, node in enumerate(test.node_names):
    print(f'{i}: {node}')
test.next_node()
print(test.current_node)
test.execute_node(input(f'Введите путь к файлу для узла {test.current_node}:\n '))
test.next_node()
test.execute_node(input(f'Введите путь к файлу для узла {test.current_node}:\n '))
test.prev_node()
test.execute_node(input(f'Введите путь к файлу для узла {test.current_node}:\n '))
# test.execute_node('test_data\\raw_qubit_amp_cal_good.pkl')
# test.execute_node('test_data\\fine_resonator_freq_cal.pkl')
# test.execute_node('test_data\\raw_qubit_amp_cal_good.pkl')
