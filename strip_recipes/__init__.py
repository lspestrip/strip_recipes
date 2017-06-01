#  -*- encoding: utf-8 -*-

'''Implementation of the ``RecipeFile`` class.'''

from datetime import datetime
from collections import namedtuple
from typing import List, Union

RecipeOp = namedtuple('RecipeOp', ['operation', 'args'])

class RecipeFile:
    '''A recipe file for the LSPE/Strip tester software.

    This class can be used to create text files containing instructions for the
    LSPE/Strip tester software used to test the Strip polarimeters.

    ``RecipeFile`` objects must be opened using the ``create_file`` method and
    closed using the ``close`` method. The best way to use them is through the
    ``open_recipe`` function.
    '''

    def __init__(self):
        '''Create a new recipe file.

        Initialize an empty recipe file with the specified file name. After the
        object has been created, you can use any of the following methods to
        put commands in the recipe:
           * ``sbs``, ``sbs_on``, ``sbs_off``
           * ``record_start``, ``record_stop``
           * ``bias_set``, ``pid_set``
           * ``rf_start_sweep``, ``rf_cw``
           * ``wait``

        When the recipe is complete, use the method ``write_to_file`` to save the
        recipe in a text file ready to be submitted to the Strip tester software.
        '''

        self.operations = []  # type: List[RecipeOp]

    def write_to_file(self, file_obj, comment=''):
        'Create the text file and set it up.'

        now = datetime.utcnow()
        comment_lines = []
        if comment != '':
            comment_lines += ['# BEGIN_COMMENT', comment, '# END_COMMENT']

        file_obj.write('''
# generation_time = "{date}"
# num_of_operations = {num}
# wait_duration_sec = {wait_time}

{comment}

TESTSET:
'''.format(date=now.strftime("%Y-%m-%dT%H:%M:%SZ"),
           num=len(self.operations),
           wait_time=sum([x.args[0] for x in self.operations
                          if x.operation.upper() == 'WAIT']),
           comment='\n'.join(comment_lines)))

        for cur_op in self.operations:
            file_obj.write('{op} {args};\n'
                           .format(op=cur_op.operation,
                                   args=', '.join([str(x) for x in cur_op.args])))

    def load_settings(self, file_name: str, pol_id: int):
        '''Load bias values for a polarimeter from the specified file name.

        Parameters:
           * file_name: name of the file containing the bias table
           * pol_id: the index (0-48) of the polarimeter
        '''

        assert isinstance(file_name, str)
        assert isinstance(pol_id, int)

        assert file_name != ''
        assert pol_id >= 0 and pol_id <= 48

        self.operations.append(RecipeOp('LoadSettings', [file_name, pol_id]))

    def sbs(self, status: bool):
        '''Turn the bias board on or off.

        Parameters:
           * file_name: name of the file containing the bias table
           * pol_id: the index (0-48) of the polarimeter
        '''

        assert isinstance(status, bool)

        status_str = {True: 'ON', False: 'OFF'}
        self.operations.append(RecipeOp('Sbs', [status_str[status]]))

    def sbs_on(self):
        'Turn the bias board on.'
        self.sbs(True)

    def sbs_off(self):
        'Turn the bias board off.'
        self.sbs(False)

    def record_start(self, name: str):
        '''Start recording operations.

        Once this command is submitted, the tester software begins the acquisition of
        the output of the polarimeter.

        Parameters:
           * ``name``: descriptive name for the test.
        '''

        assert isinstance(name, str)
        assert name != ''

        self.operations.append(RecipeOp('RecordStart', [name]))

    def record_stop(self):
        'Stop recording operations.'

        self.operations.append(RecipeOp('RecordStop', []))

    def bias_set(self, target: str, value: Union[float, int]):
        '''Set a bias to some value.

        The biases currently accepted by the program are the following, together with the
        measure unit to be used with "value" (case is ignored):
        * "HA1_Vd", …, "HB3_Vd": HEMT drain voltage [mV]
        * "HA1_Id", …, "HB3_Id": HEMT drain current [mA]
        * "HA1_Vg", …, "HB3_Vg": HEMT gate voltage [mV]
        * "HA3bis_Vg", "HB3bis_Vg": HEMT #3 second gate voltage [mV]
        * "PSA1_Vr", …, "PSB2_Vr": Reverse bias of the PH/SW diode [mV]
        * "PSA1_If", …, "PSB2_If": Direct current of the PH/SW diode [mA]
        * "Q1_bias", …, "Q2_bias": Bias voltage of the detector diode, from 0 to 4095 [ADU]
        * "Q1_offset", …, "Q2_offset": Preamplifier bias offset, from 0 to 4095 [ADU]
        * "Q1_gain", …. "Q2_gain": Preamplifier gain (not implemented), from 0 to 255 [ADU]
        '''

        assert isinstance(target, str)
        assert isinstance(value, int) or isinstance(value, float)

        self.operations.append(RecipeOp('BiasSet', [target, value]))

    def pid_set(self, target: str, temperature: Union[float, int]):
        '''Set the temperature of a PID.

        The four PIDs recognized by the program are:
           * LA
           * LB
           * Lcross
           * Lpol
        Case is ignored.
        '''

        assert isinstance(target, str)
        assert isinstance(temperature, float) or isinstance(temperature, int)

        assert target.upper() in ['LA', 'LB', 'LCROSS', 'LPOL']
        assert temperature > 0.0

        self.operations.append(RecipeOp('PidSet', [target, temperature]))

    def rf_start_sweep(self, 
                       fmin: Union[float, int], 
                       fmax: Union[float, int], 
                       step: Union[float, int], 
                       dwell: Union[float, int], 
                       power: Union[float, int]):
        '''Start a frequency sweep using the swept generator.

        Parameters:
           * fmin: Start frequency (in GHz)
           * fmax: End frequency (in GHz)
           * step: Step frequency (in GHz)
           * dwell: Time to wait for each step (in ms)
           * power: power used by the generator (in dBm)
        '''

        assert isinstance(fmin, float) or isinstance(fmin, int)
        assert isinstance(fmax, float) or isinstance(fmax, int)
        assert isinstance(step, float) or isinstance(step, int)
        assert isinstance(dwell, float) or isinstance(dwell, int)
        assert isinstance(power, float) or isinstance(power, int)

        assert fmin > 0.0
        assert step > 0.0
        assert dwell > 0.0
        assert fmin < fmax
        assert step < (fmax - fmin)

        self.operations.append(RecipeOp('RfStartSweep',
                                        [fmin, fmax, step, dwell, power]))

    def rf_cw(self, status: bool, freq: Union[float, int], power: Union[float, int]):
        '''Switch the swept generator on or off using a fixed frequency.

        Parameters:
           * status: True to turn the generator ON, False otherwise
           * freq: Frequency to inject (in GHz)
           * power: power used by the generator (in dBm)
        '''

        assert isinstance(status, bool)
        assert isinstance(freq, float) or isinstance(freq, int)
        assert isinstance(power, float) or isinstance(power, int)

        assert freq > 0.0

        status_str = {True: 'ON', False: 'OFF'}
        self.operations.append(RecipeOp('RfCw', [status_str[status], freq, power]))


    def wait(self, time: Union[float, int]):
        'Wait for the specified time (in seconds).'

        assert isinstance(time, float) or isinstance(time, int)

        assert time >= 0.0

        self.operations.append(RecipeOp('Wait', [time]))
