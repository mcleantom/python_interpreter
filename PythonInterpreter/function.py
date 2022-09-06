import inspect
import types
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PythonInterpreter import VirtualMachine
else:
    VirtualMachine = None

__all__ = ["Function"]


class Function:
    def __init__(self, name, code, globs, defaults, closure, vm):
        self._vm: VirtualMachine = vm
        self.func_code = code
        self.func_name = self.__name__ = name or code.co_name
        self.func_defaults = tuple(defaults)
        self.func_globals = globs
        self.func_locals = self._vm.frame.f_locals
        self.__dict__ = {}
        self.func_closure = closure
        self.__doc__ = code.co_consts[0] if code.co_consts else None

        kw = {"argdefs": self.func_defaults}
        if closure:
            kw["closure"] = tuple(make_cell(0) for _ in closure)
        self._func = types.FunctionType(code, globs, **kw)

    def __call__(self, *args, **kwargs):
        call_args = inspect.getcallargs(self._func, *args, **kwargs)
        frame = self._vm.make_frame(self.func_code, call_args=call_args, global_names=self.func_globals, local_names={})
        return self._vm.run_frame(frame)


def make_cell(value):
    ...
