from multiprocessing.connection import Listener
import traceback, os, time, zlib
from queue import Queue
from itertools import count
from threading import Thread
from tool import log
from render import init_driver
from interface import IRequest, IPageResult
from datetime import datetime

l = log("FirstPy")

DATA = {}

NAME = "/tmp/work_socket"
if os.path.exists(NAME):
    os.remove(NAME)

q_input = Queue()
driver = init_driver( headless=False )
# driver.implicitly_wait(10)
driver.set_page_load_timeout(10)


def work(*args, **kwargs):
    request = args[0]
    driver.get(request.url)
    if request.jscript:
        breakpoint()
        driver.execute_script( request.jscript )
        time.sleep(1)
    time.sleep( request.wait )
    DATA[ request.id ] = {
        "data" : zlib.compress( driver.page_source.encode("utf8") ), 
        "expiration_date" : request.expiration_date 
    }
    

def queue_service():

    for c in count():
        item = q_input.get()
        req = IRequest( **item )
        try:
            work( req )
            l.info(f"item: {str(item)} req: {req}")
        except Exception as e:
            l.error("Error", exc_info=True)

def clear_service():

    for c in count():
        # l.info(f"Clear DATA len [{len(DATA)}]")
        for k in list( DATA.keys() ):
            if DATA[k]["expiration_date"] < datetime.now().timestamp():
                DATA.pop( k )

        # l.info(f"Finish DATA len [{len(DATA)}]")
        time.sleep(60)


def get_result(page):
    result = None
    if DATA.get( page.id ):
        result = DATA.get( page.id )
        result = result["data"]
    return result



def echo_client(conn):
    try:
        while True:
            payload = conn.recv()
            if payload.get("url"):
                q_input.put( payload )
            else:
                page = IPageResult(id=payload['id'])
                conn.send( get_result( page ) )

            # conn.send( payload )
    except EOFError:
        l.info("Connected close")

def echo_server(address, authkey):
    serv = Listener(address, authkey=authkey)
    while True:
        try:
            client = serv.accept()
            Thread(target=echo_client, args=(client,)).start()
            # echo_client( client )

        except Exception:
            traceback.print_exc()
            # l.error("Error", exc_info=True)
            # serv.close()
            # pass


def main():
    try:
        l.info(f"Start server: {NAME}")
        Thread(target=queue_service, daemon=True).start()
        Thread(target=clear_service, daemon=True).start()
        echo_server( NAME, authkey=b'qwerty' )
    finally:
        driver.quit()
        l.info("Drop process")

if __name__ == '__main__':
    main()
