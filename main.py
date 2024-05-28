from nodes_manager import NodesManager

test = NodesManager()
test.add_nodes([
    'RawResonatorFreqCalNode',
    'RawQubitFreqCalNode',
    'RawQubitAmpCalNode',
    'AccurateResonatorFreqCalNode',
    'AccurateQubitAmpCalNode',
    'IQCalNode',
    'PreciselyQubitAmpCalNode',
    'RamseyQubitFreqCalNode',
])
print(test.node_names)
test.next_node()
# test.execute_node('test_data\\raw_resonator_freq_cal.pkl')
test.next_node()
# test.execute_node('test_data\\raw_qubit_freq_cal_bad.pkl')
test.next_node()
# test.execute_node('test_data\\raw_qubit_amp_cal_bad.pkl')
test.next_node()
# test.execute_node('test_data\\fine_resonator_freq_cal.pkl')
test.next_node()
# test.execute_node('test_data\\fine_qubit_amp_cal.pkl')
test.next_node()
# test.execute_node('test_data\\cal_curves_3.pkl')
test.next_node()
# test.execute_node('test_data\\very_fine_qubit_amp_cal_N=201.pkl')
test.next_node()
test.execute_node('test_data\\ramsey_2.pkl')
