import os
from fnmatch import fnmatch

if __name__=='__main__':
    print(__file__ + "=>")

    print( os.listdir() )
    rel_path = os.path.join('venv', 'Scripts'  )
    print(f"{rel_path=}")

    os.chdir( rel_path )
    print( f"{os.listdir()=}" )

    print( [name for name in os.listdir() if fnmatch(name,"*.exe")] )

    


