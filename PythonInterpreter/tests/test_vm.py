import dis
import textwrap
import types
from unittest import TestCase

from PythonInterpreter import VirtualMachine


def dis_code(code):
    """Disassemble `code` and all the code it refers to."""
    for const in code.co_consts:
        if isinstance(const, types.CodeType):
            dis_code(const)

    print("")
    print(code)
    dis.dis(code)


class TestVM(TestCase):
    def setUp(self):
        self.vm = VirtualMachine()

    def run_code_str(self, code: str):
        code = textwrap.dedent(code)
        code = compile(code, f"<{self.id()}>", "exec", 0, 1)
        dis_code(code)
        return self.vm.run_code(code)

    def test_mod(self):
        res = self.run_code_str(
            """\
        def fn(a, b):
            return a%b
        fn(10, 5)
        """
        )
        self.vm.run_code(dis.dis("10%5"))
