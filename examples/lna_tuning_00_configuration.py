#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import sys

from strip_recipes import RecipeFile

PHASE_SWITCH_REVERSE_VOLTAGE = -1.8e3 # mV
PHASE_SWITCH_FORWARD_CURRENT = 1.0 # mA
ADC_BIAS = 1000 # ADU
ADC_OFFSET = 0 # ADU


def main(args):
	base_file_name = 'pol_lna_tuning_00_setup'
	recipe_file_name = base_file_name + '.recipe'
	
	recipe = RecipeFile()
	recipe.record_start(base_file_name)
	recipe.sbs_on()

	# Wait a few seconds to record the data and check that everything is ok
	recipe.wait(10)
	
	# Set up the PH/SW
	for phsw in ('A1', 'A2', 'B1', 'B2'):
		recipe.bias_set('PS{0}_Vr'.format(phsw), PHASE_SWITCH_REVERSE_VOLTAGE)
		recipe.bias_set('PS{0}_If'.format(phsw), PHASE_SWITCH_FORWARD_CURRENT)
		# This is not implemented yet
		# recipe.bias_set('PS{0}_Drive'.format(phsw), 0)

	# Set up the ADCs
	for adc in ('Q1', 'Q2', 'U1', 'U2'):
		recipe.bias_set('{0}_bias'.format(adc), ADC_BIAS)
		recipe.bias_set('{0}_offset'.format(adc), ADC_OFFSET)

	# Wait a few seconds to record the data and check that everything is ok
	recipe.wait(10)
	recipe.sbs_off()
	recipe.record_stop()

	# Read this very script
	with open(__file__, 'rt') as f:
		this_script = f.readlines()

	# Save the recipe and include this script in the comments
	with open(recipe_file_name, "wt") as f:
		recipe.write_to_file(f, source_script=''.join(this_script))
		
	print('Recipe written to file "{0}"'.format(recipe_file_name))
	
if __name__ == '__main__':
	main(sys.argv[1:])
