import traceback
try:
    import app
    print('imported app:', app)
    print('attrs:', [k for k in app.__dict__ if not k.startswith('__')])
except Exception as e:
    print('exception importing app:', type(e), e)
    traceback.print_exc()