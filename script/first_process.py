from multiprocessing.connection import Listener
import traceback, os, time, zlib
from queue import Queue
from itertools import count
from threading import Thread
from tool import log
from render import init_driver
from interface import IRequest, IPageResult
from datetime import datetime
from  concurrent.futures import ThreadPoolExecutor

def init(*args):
    headless = args[0]

    l = log("FirstPy")

    DATA = {}

    NAME = ("localhost", 25100)
    # if os.path.exists(NAME):
    #     os.remove(NAME)

    q_input = Queue()
    driver = init_driver( headless=headless )
    # driver.implicitly_wait(10)
    driver.set_page_load_timeout(10)


    def work( request ):
        # request = args[0]
        driver.get(request.url)
        time.sleep( request.wait )
        
        if request.jscript:
            driver.execute_script( request.jscript )
            time.sleep(1)

        DATA[ request.id ] = {
            "data" : zlib.compress( driver.page_source.encode("utf8") ), 
            "expiration_date" : request.expiration_date 
        }


    def work_service():

        for c in count():
            item = q_input.get()
            req = item
            try:
                work( req )
                l.info(f"item: {str(item)} req: {req}")
            except Exception as e:
                l.error("Error", exc_info=True)

    
    def get_active_content( param: IRequest ):
        if param.jscript:
            driver.execute_script( param.jscript )
            time.sleep(param.wait)

        return driver.page_source


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
                
                method = payload.get("method")
                
                if method == "render":
                    q_input.put( IRequest( **payload) )
                
                if method == "result":
                    page = IPageResult(**payload)
                    conn.send( get_result( page ) )

                if method == "active_content":
                    data = get_active_content( IRequest(**payload) )
                    conn.send( data )

                # conn.send( payload )
        except EOFError:
            l.info("Connected close")

    def echo_server(address, authkey):
        serv = Listener(address, authkey=authkey)

        with ThreadPoolExecutor(max_workers=4) as executor:

            for _ in count():
                try:
                    client = serv.accept()
                    executor.submit(echo_client, client)
                except Exception:
                    traceback.print_exc()


    def main():
        try:
            l.info(f"Start server: {NAME}")
            Thread(target=work_service, daemon=True).start()
            Thread(target=clear_service, daemon=True).start()
            echo_server( NAME, authkey=b'qwerty' )
        finally:
            driver.quit()
            l.info("Drop process")

    return main

if __name__ == '__main__':
    main = init()
    main()
