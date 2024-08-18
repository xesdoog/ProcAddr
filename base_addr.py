import os
import psutil
import pymem
import sys
from threading import Thread
from time      import sleep

pid      = 0
procname = ""

def proc_scan_msg():
    print("", end = f'\rScanning process tree _', flush = True)
    sleep(0.05)   
    print("", end = f'\rScanning process tree \\', flush = True)
    sleep(0.05)
    print("", end = f'\rScanning process tree |', flush = True)
    sleep(0.05)
    print("", end = f'\rScanning process tree /', flush = True)
    sleep(0.05)
    print("", end = f'\rScanning process tree _', flush = True)
    sleep(0.05)   
    print("", end = f'\rScanning process tree \\', flush = True)
    sleep(0.05)
    print("", end = f'\rScanning process tree |', flush = True)
    sleep(0.05)
    print("", end = f'\rScanning process tree /', flush = True)
    sleep(0.05)

def get_base_address(procname):
    global pid
    for p in psutil.process_iter(['pid', 'name', 'exe', 'cmdline']):
        if (
            procname == p.info['name'] or p.info["exe"]
                and os.path.basename(p.info["exe"]) == procname
                or p.info["cmdline"]
                and p.info["cmdline"][0] == procname
        ):
            pid = p.pid
            break
    else:
        pid = 0
        proc_scan_msg()


    if pid != 0:
        pm = pymem.Pymem()
        pm.open_process_from_id(pid)
        base_address = pm.base_address
        pm.close_process()

        return hex(base_address).upper().replace('X', 'x')
    else:
        return None

def main_program():
    try:
        procname = input(f'Please enter the process name (names are case sensitive): ')
        if procname != "":
            if not procname.endswith('.exe'):
                procname = procname + '.exe'
                
            baseAddr = get_base_address(procname)
            if baseAddr is not None:
                print(f"\rProcess Name: {procname}\nBase Address: {baseAddr}")
                sys.exit(0)
            else:
                print ("", end = f'\rProcess {procname} is not running.', flush = True)
                sys.exit(0)

    except Exception as exc:
        print(f'An error has occured! {exc}')


if __name__ == "__main__":
    main_program()
