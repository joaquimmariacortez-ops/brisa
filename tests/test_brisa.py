import io
import unittest
from contextlib import redirect_stdout

from brisa import BrisaError, run


class BrisaTests(unittest.TestCase):
    def execute(self, source):
        output = io.StringIO()
        with redirect_stdout(output):
            run(source)
        return output.getvalue()

    def test_runs_a_program_saved_as_text(self):
        output = self.execute('crie nome = "Lua"\ndiga "Olá, " + nome\n')
        self.assertEqual(output, "Olá, Lua\n")

    def test_repeats_an_indented_block(self):
        output = self.execute("repita 2:\n  diga 4 * 5\n")
        self.assertEqual(output, "20\n20\n")

    def test_rejects_unknown_instruction(self):
        with self.assertRaisesRegex(BrisaError, "não entendi"):
            run("salte\n")
