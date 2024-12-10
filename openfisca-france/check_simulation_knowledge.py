from new_simulation import simulation as nude_simulation


input_variable_not_set = nude_simulation.menage.get_holder('loyer').get_array('2022-01')
assert input_variable_not_set is None
