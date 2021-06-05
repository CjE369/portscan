#Multithreaded Port Scanner
from queue import Queue
from socket import *
import socket
import threading

target = input("Enter target ip:")
target = "127.0.0.1"
specific_port = []
specific_port = input(" Enter specific port you want to scan (if you have) press enter to skip this step: ")

if len(specific_port) == 0:
    queue = Queue()
    open_ports = []


    def portscan(port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((target, port))
            return True
        except:
            return False


    def get_ports(mode):
        if mode == 1:
            for port in range(1, 1024):
                queue.put(port)
        elif mode == 2:
            for port in range(1, 49152):
                queue.put(port)
        elif mode == 3:
            ports = [20, 21, 22, 23, 25, 53, 80, 110, 443]
            for port in ports:
                queue.put(port)
        elif mode == 4:
            ports = input("Enter your ports (seperate by blank):")
            ports = ports.split()
            ports = list(map(int, ports))
            for port in ports:
                queue.put(port)


    def worker():
        while not queue.empty():
            port = queue.get()
            if portscan(port):
                print("Port {} is open!".format(port))
                open_ports.append(port)


    def run_scanner(threads, mode):

        get_ports(mode)

        thread_list = []

        for t in range(threads):
            thread = threading.Thread(target=worker)
            thread_list.append(thread)

        for thread in thread_list:
            thread.start()

        for thread in thread_list:
            thread.join()

        print("Open ports are:", open_ports)


    run_scanner(100, 1)

else:

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def spec_port_check():
        try:
            s.connect(target, specific_port)
            return True
        except:
            return False

    if spec_port_check() == True:
        print("Port ", specific_port, " is opean")
    else:
        print(specific_port, "is closed")