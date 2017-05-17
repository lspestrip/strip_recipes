#  -*- encoding: utf-8 -*-

'''Implementation of the ``RecipeFile`` class.'''

from datetime import datetime

class RecipeFile:
    '''A recipe file for the LSPE/Strip tester software.

    This class can be used to create text files containing instructions for the
    LSPE/Strip tester software used to test the Strip polarimeters.

    ``RecipeFile`` objects should be used in a ``with`` block, like in the following example::

        with RecipeFile('out.txt') as f:
            f.record_start(10.0)
            f.record_stop()

        # Now file 'out.txt' is ready to be used.
    '''

    def __init__(self, file_name: str):
        '''Create a new recipe file.

        Initialize an empty recipe file with the specified file name. The object
        is meant to be used within a "with" block, in order to properly open and
        close the text file specified by "file_name".
        '''

        self.file_name = file_name
        self.instruction_idx = None
        self.filehandle = None

    def __enter__(self):
        self.filehandle = open(self.file_name, "wt")

        now = datetime.utcnow()
        self.filehandle.write('''
# Recipe generated on {date}

TESTSET:
'''.format(date=now.strftime("%Y-%m-%d %H:%M:%S UTC")))

    def __exit__(self, exc_type, exc_value, traceback):
        self.filehandle.close()

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

        self.filehandle.write('LoadSettings\t{file_name}, {pol_id};\n'
                              .format(file_name=file_name, pol_id=pol_id))
        self.instruction_idx += 1

    def sbs(self, status: bool):
        '''Turn the bias board on or off.

        Parameters:
           * file_name: name of the file containing the bias table
           * pol_id: the index (0-48) of the polarimeter
        '''
        assert isinstance(status, bool)

        status_str = {True: 'ON', False: 'OFF'}
        self.filehandle.write('Sbs\t{0};\n'.format(status_str[status]))
        self.instruction_idx += 1

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

        self.filehandle.write('RecordStart\t{0};\n'.format(name))
        self.instruction_idx += 1

    def record_stop(self):
        'Stop recording operations.'

        self.filehandle.write('RecordStop;\n')
        self.instruction_idx += 1

    def bias_set(self, target: str, value: float):
        '''Set a bias to some value.'''

        assert isinstance(target, str)
        assert isinstance(value, int) or isinstance(value, float)

        self.filehandle.write('BiasSet\t{target}, {value};\n'
                              .format(target=target, value=value))
        self.instruction_idx += 1

    def pid_set(self, target: str, temperature: float):
        '''Set the temperature of a PID.

        The four PIDs recognized by the program are:
           * LA
           * LB
           * Lcross
           * Lpol
        Case is ignored.
        '''

        assert isinstance(target, str)
        assert isinstance(temperature, float)

        assert target.upper() in ['LA', 'LB', 'LCROSS', 'LPOL']
        assert temperature > 0.0

        self.filehandle.write('PidSet\t{target}, {temperature}'
                              .format(target=target, temperature=temperature))
        self.instruction_idx += 1

    def rf_start_sweep(self, fmin: float, fmax: float, step: float, dwell: float, power: float):
        '''Start a frequency sweep using the swept generator.

        Parameters:
           * fmin: Start frequency (in GHz)
           * fmax: End frequency (in GHz)
           * step: Step frequency (in GHz)
           * dwell: Time to wait for each step (in ms)
           * power: power used by the generator (in dBm)
        '''

        assert isinstance(fmin, float)
        assert isinstance(fmax, float)
        assert isinstance(step, float)
        assert isinstance(dwell, float) or isinstance(dwell, int)
        assert isinstance(power, float) or isinstance(power, int)

        assert fmin > 0.0
        assert step > 0.0
        assert dwell > 0.0
        assert fmin < fmax
        assert step < (fmax - fmin)

        self.filehandle.write('RfStartSweep\t{fmin}, {fmax}, {step}, {dwell}, {power};\n'
                              .format(fmin=fmin, fmax=fmax, step=step, dwell=dwell, power=power))
        self.instruction_idx += 1

    def rf_cw(self, status: bool, freq: float, power: float):
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
        self.filehandle.write('RfCw\t{status}, {freq}, {power};\n'
                              .format(status=status_str[status], freq=freq, power=power))

    def wait(self, time: float):
        'Wait for the specified time (in seconds).'

        assert isinstance(time, float) or isinstance(time, int)

        assert time >= 0.0
        self.filehandle.write('Wait\t{0};\n'.format(time))
        self.instruction_idx += 1
