from importlib.abc import Loader
from importlib.util import LazyLoader
from importlib.machinery import ModuleSpec
from types import ModuleType
import sys, logging

class CloudLoader(LazyLoader):
    
    def __init__(self, fullname: str, source_code: str, url: str) -> None:
        self.fullname = fullname
        self.source_code = source_code
        self.url = url

    def create_module(self, spec: ModuleSpec | None = None) -> ModuleType | None:
        module = sys.modules.get(spec.name)
        if module is None:
            module = ModuleType(spec.name)
            sys.modules[spec.name] = module
        return module
    
    def exec_module(self, module: ModuleType) -> ModuleType | None:
        module.__file__ = self.url
        exec(self.source_code, module.__dict__)
        return module
    
    def get_source(self, name: str) -> str | None:
        s = compile(self.source_code, self.url, 'exec')
        return self.source_code
