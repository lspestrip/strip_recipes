from strip_recipes import RecipeFile

recipe = RecipeFile()
recipe.record_start('NOISE_TEMPERATURE')

# Turn on the bias board
recipe.sbs_on()

# Set the temperature of the heater A to 20 K
recipe.pid_set('LA', 20)

# Wait some time (in seconds)
recipe.wait(600)

# Increase the temperature to 40 K
recipe.pid_set('LA', 40)

recipe.wait(600)

recipe.sbs_off()
recipe.record_stop()

with open(__file__, 'rt') as f:
    this_script = f.readlines()

with open('recipe.txt', 'wt') as f:
    recipe.write_to_file(f, source_script=''.join(this_script))
    