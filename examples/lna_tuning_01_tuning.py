#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import sys

import numpy as np
from collections import namedtuple
from strip_recipes import RecipeFile

TEMPERATURE_STEPS = (10.0, 20.0, 30.0, 40.0) # K
THERMALIZATION_WAIT_TIME = 300.0 # s
BIAS_WAIT_TIME = 10.0 # s

RampConf = namedtuple('RampConf', 'start stop steps')

def input_int(prompt: str) -> int:
	return int(input(prompt))
	
def input_float(prompt: str) -> float:
	return float(input(prompt))
	
def value_list_for_ramp(ramp: RampConf, reverse=False):
	if reverse:
		return np.linspace(ramp.stop, ramp.start, ramp.steps)
	else:
		return np.linspace(ramp.start, ramp.stop, ramp.steps)

def input_ramp(parameter_name, amplifier_name) -> RampConf:
	start = input_float('Minimum {param} [mV] to use for {amp}: '
						.format(param=parameter_name, amp=amplifier_name))
	stop = input_float('Maximum {param} [mV] to use for {amp}: '
					   .format(param=parameter_name, amp=amplifier_name))
	steps = input_int('Number of {param} steps to use for {amp}: '
					  .format(param=parameter_name, amp=amplifier_name))
	return RampConf(start, stop, steps)
	
def main(args):
	if len(args) > 1:
		print('''You cannot specify more than one command line parameter.
If this parameter is present, it will be interpreted as the
number of the polarimeter to be tested.
''')

	if len(args) == 1:
		pol_number = int(args[0])
	else:
		pol_number = input_int('Enter the number of the polarimeter being tested: ')

	drain_conf = {}
	gate_conf = {}
	comment_lines = []
	for cur_amplifier in ('HA1', 'HB1'):
		print('* * * {0} * * *'.format(cur_amplifier))
		
		ramp = input_ramp('Vdrain', cur_amplifier)
		values = value_list_for_ramp(ramp)
		print('The values to be explored are the following: {0}'
		      .format(', '.join([str(x) for x in values])))
		drain_conf[cur_amplifier] = ramp

		comment_lines.append('Vdrain ramp for {0}: {1} ({2})'
					 .format(cur_amplifier, ramp, values))

		print('')
		ramp = input_ramp('Vgate', cur_amplifier)
		values = value_list_for_ramp(ramp)
		print('The values to be explored are the following: {0}'
		      .format(', '.join([str(x) for x in values])))
		gate_conf[cur_amplifier] = ramp
		
		print('')

		comment_lines.append('Vgate ramp for {0}: {1} ({2})'
		                     .format(cur_amplifier, ramp, values))
		
		
	base_file_name = 'pol{0:02d}_lna_tuning_01_tuning'.format(pol_number)
	recipe_file_name = base_file_name + '.recipe'
	
	recipe = RecipeFile()
	recipe.record_start(base_file_name)
	recipe.sbs_on()

	# Wait a few seconds to record the data and check that everything is ok
	recipe.wait(10)

	for cur_temperature in TEMPERATURE_STEPS:
		recipe.pid_set('LA', cur_temperature)
		recipe.pid_set('LB', cur_temperature)
		recipe.wait(THERMALIZATION_WAIT_TIME)
		
		for cur_amplifier in ('HA1', 'HB1'):
			for idx, cur_drain in enumerate(value_list_for_ramp(drain_conf[cur_amplifier])):
				recipe.bias_set('{0}_Vg'.format(cur_amplifier), cur_drain)

				reverse = idx % 2 == 0
				for cur_gate in value_list_for_ramp(gate_conf[cur_amplifier], reverse=reverse):
					recipe.bias_set('{0}_Vg'.format(cur_amplifier), cur_gate)
					
					recipe.wait(BIAS_WAIT_TIME)

	recipe.sbs_off()
	recipe.record_stop()

	# Read this very script
	with open(__file__, 'rt') as f:
		this_script = f.readlines()

	print(comment_lines)
	
	# Save the recipe and include this script in the comments
	with open(recipe_file_name, "wt") as f:
		recipe.write_to_file(f, comment_lines=comment_lines,
		                     source_script=''.join(this_script))
		
	print('Recipe written to file "{0}"'.format(recipe_file_name))
	
if __name__ == '__main__':
	main(sys.argv[1:])
