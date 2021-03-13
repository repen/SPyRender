"""
Copyright 2021 Andrey Plugin (9keepa@gmail.com)
Licensed under the Apache License v2.0
http://www.apache.org/licenses/LICENSE-2.0
"""
from multiprocessing import Process, Lock
from tool import log as _log
import time

log = _log("MAIN")

def proc1():
    from first_process import main
    main()

def proc2():
    from flasksrv import app_run
    app_run()

def main():
    p1 = Process( target=proc1, daemon=True)
    p2 = Process( target=proc2, daemon=True )

    p1.start()
    time.sleep(5)
    p2.start()    

    p1.join()
    p2.join()

if __name__ == '__main__':
    main()