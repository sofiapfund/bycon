# import importlib.util

# file_path = 'biosamples.py'
# module_name = 'biosamples'

# spec = importlib.util.spec_from_file_location(module_name, file_path)
# module = importlib.util.module_from_spec(spec)
# spec.loader.exec_module(module)

# module.biosamples('biosamples')

# f = getattr(module, 'biosamples')

# f('biosamples')

# modbiosamples('biosamples')


from importlib import import_module


mod = import_module('collations')
f = getattr(mod, 'collations')

f('collations')