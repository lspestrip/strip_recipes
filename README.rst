Strip test recipes
==================

This Python package allows to easily create recipes for the LSPE/Strip tester software.


Installation
============

Download the package and run the following command::

    python setup.py install 

If you plan to work on the source code, you should instead use the following command to
install it:

    pip install -e .


Running the test suite
======================

In order to run the test suite, you must have the Nose library installed. To run the
tests, issue the following command::

    python setup.py test

Example
=======

The library is extremely easy to use. It implements a number of checks on the parameters
passed to the commands to be put in the recipe file (e.g., it forbids negative temperatures).

The following is a minimal working example which shows how the library should be used:

.. code-block:: python

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

    with open('recipe.txt', 'wt') as f:
        recipe.write_to_file(f)


After the execution of the script, file ``recipe.txt`` will contain the following text::

    # generation_time = 2017-01-01T00:00:00Z
    # num_of_operations = 8
    # wait_duration_sec = 1200

    TESTSET:
    RecordStart NOISE_TEMPERATURE;
    Sbs ON;
    PidSet LA, 20;
    Wait 600;
    PidSet LA 40;
    Wait 600;
    Sbs OFF;
    RecordStop ;

It is possible to record additional comments in the file, using the keyword
`comment_lines` when calling `RecipeFile.write_to_file`. The parameter
accepts a list of strings: each one will be saved at the beginning of the
recipe file, prepended by an hash character (`#`).

It is easy to embed the source code of the Python file used to generate the
program in the recipe itself using the keyword `source_script`:

.. code-block:: python

    with open(__file__, 'rt') as f:
        this_script = f.readlines()

    with open('recipe.txt', 'wt') as f:
        recipe.write_to_file(f, source_script=''.join(this_script))
