import contextlib
import io
from unittest import TestCase

from PythonInterpreter import Interpreter


class TestInterpreter(TestCase):
    def setUp(self) -> None:
        self.interpreter = Interpreter()

    def test_addition(self):
        what_to_execute = {
            "instructions": [
                ("LOAD_VALUE", 0),
                ("LOAD_VALUE", 1),
                ("ADD_TWO_VALUES", None),
                ("LOAD_VALUE", 2),
                ("ADD_TWO_VALUES", None),
                ("PRINT_ANSWER", None),
            ],
            "numbers": [7, 5, 8],
        }

        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            result = self.interpreter.run_code(what_to_execute)

        self.assertEqual(sum(what_to_execute["numbers"]), float(f.getvalue()))

    def test_variables(self):
        a = 1
        b = 3
        what_to_execute = {
            "instructions": [
                ("LOAD_VALUE", 0),
                ("STORE_NAME", 0),
                ("LOAD_VALUE", 1),
                ("STORE_NAME", 1),
                ("LOAD_NAME", 0),
                ("LOAD_NAME", 1),
                ("ADD_TWO_VALUES", None),
                ("PRINT_ANSWER", None),
            ],
            "numbers": [a, b],
            "names": ["a", "b"],
        }
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            self.interpreter.run_code(what_to_execute)
        self.assertEqual(a + b, float(f.getvalue()))
