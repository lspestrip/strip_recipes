# -*- encoding: utf-8 -*-

from unittest import TestCase
from io import StringIO
from typing import List

from strip_recipes import RecipeFile

def split_script(text: str) -> List[str]:
    'Split a string containing a recipe in a list of nonempty lines.'
    return [x.strip() for x in text.split('\n') if x != '']

class TestRecipeFile(TestCase):
    def test_basic_operations(self):
        'Check that the code is able to correctly write a simple recipe into a file'

        buf = StringIO()
        rec = RecipeFile()
        rec.record_start('TSYS')
        rec.record_stop()

        rec.write_to_file(buf, comment_lines=['Hello, world!'])

        result = split_script(buf.getvalue())
        for idx, line in enumerate(result):
            if line.startswith('# generation_time ='):
                # Drop the line, because it contains a time-dependent string
                # which is not easy to test
                del result[idx]
                break

        expected = ['# num_of_operations = 2',
                    '# wait_duration_sec = 0',
                    '# Hello, world!',
                    'TESTSET:',
                    'RecordStart TSYS;',
                    'RecordStop ;']

        self.assertEqual(len(result), len(expected))
        for idx, cur_line in enumerate(result):
            self.assertEqual(cur_line, expected[idx])

    def test_wait_time(self):
        'Check that the overall wait time saved in the recipe file is calculated correctly'

        buf = StringIO()
        rec = RecipeFile()

        rec.record_start('WAITTEST')
        rec.wait(5)
        rec.sbs_on()
        rec.wait(9)
        rec.sbs_off()
        rec.record_stop()

        rec.write_to_file(buf)

        result = [x for x in split_script(buf.getvalue()) if x.startswith('# wait_duration_sec =')]
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], '# wait_duration_sec = 14')
