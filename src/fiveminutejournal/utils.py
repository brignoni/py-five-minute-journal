import importlib
import pkgutil
import fiveminutejournal.plugins
from fiveminutejournal.journal import JournalConfig

def iter_namespace(ns_pkg):
    return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")


plugins = {
    name: importlib.import_module(name)
    for finder, name, ispkg
    in iter_namespace(fiveminutejournal.plugins)
}

def get_plugin(config: JournalConfig, name: str = 'default'):
    try:
        module_name = f'fiveminutejournal.plugins.{name}'
        return getattr(plugins.get(module_name), 'Plugin')(config)
    except:        
        raise Exception(f'Plugin not found: {module_name}')