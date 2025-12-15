import importlib, inspect, sys
print('cwd:', sys.path[0])
print('sys.path snippet:', sys.path[:5])
try:
    m = importlib.import_module('app')
    print('module file:', m.__file__)
    keys = [k for k in m.__dict__.keys() if not k.startswith('__')]
    print('keys:', keys)
    print('has create_app:', 'create_app' in m.__dict__)
    print('\nsource of module:')
    print(inspect.getsource(m))
except Exception as e:
    print('import error:', type(e), e)
    import traceback; traceback.print_exc()
    sys.exit(1)
