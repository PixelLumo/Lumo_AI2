import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
print('sys.path last entry:', sys.path[-1])
try:
    from app import create_app
    print('import succeeded, create_app callable?', callable(create_app))
except Exception as e:
    print('import failed:', type(e), e)
    import traceback; traceback.print_exc()
