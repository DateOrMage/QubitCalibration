from nodes_manager import NodesManager

test = NodesManager()
test.add_node('RawQubitAmpCalNode')
test.add_node('AccurateResonatorFreqCalNode')
test.next_node()
test.execute_node('test_data\\raw_qubit_amp_cal_good.pkl')
test.next_node()
test.execute_node('test_data\\fine_resonator_freq_cal.pkl')
test.prev_node()
test.execute_node('test_data\\raw_qubit_amp_cal_good.pkl')
