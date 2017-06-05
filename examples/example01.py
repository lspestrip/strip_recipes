from strip_recipes import RecipeFile

recipe = RecipeFile()
recipe.record_start('example01')
recipe.sbs_on()

for cur_gate in (10.0, 20.0, 50.0):
	recipe.bias_set('HA1_Vg', cur_gate)
	
	recipe.wait(10.0)

recipe.sbs_off()
recipe.record_stop()

with open('out.txt', 'wt') as fout:
	recipe.write_to_file(fout)