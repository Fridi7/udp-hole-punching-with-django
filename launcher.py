import socket
import threading
import requests
import os
import time
import datetime

from random import randint
from json import loads, dumps


def ip_generator():
    a, b, c, d = randint(0, 255), randint(0, 255), randint(0, 255), randint(0, 255)
    return f"{str(a)}.{str(b)}.{str(c)}.{str(d)}"


def receive_data(sock):
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            data_j = loads(data.decode('utf-8'))
            print(f"{data_j['user']} "
                  f"[{datetime.datetime.fromtimestamp(data_j['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}]: {data_j['data']}")
        except:
            pass


def prepare_connect():
    host = socket.gethostbyname(socket.gethostname())
    # host = ip_generator()  # генератор
    port = randint(6000, 10000)
    print(f'Server hosting on IP-> {str(host)}:{str(port)}')
    name = input('Please, write your name here: ')
    return name, host, port


def connect(host, port, name, server, selector):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    s.bind((host, int(port)))
    print('Server Running...')
    while True:
        if not selector:
            data, addr = s.recvfrom(1024)
            clients = []
            if addr not in clients:
                clients.append(addr)
            server = addr

        while True:
            s.sendto(name.encode('utf-8'), server)
            print("connection established with:")
            print(server)
            threading.Thread(target=receive_data, args=(s,)).start()
            while True:
                data = input()
                if data == 'qqq':
                    break
                elif data == '':
                    continue
                data = {
                    "user": name,
                    "data": data,
                    "timestamp": int(time.time())
                }
                data = dumps(data)
                s.sendto(data.encode('utf-8'), server)
            s.close()
            raise SystemExit


def run():
    selector = input('if you want to connect to the user who has already initiated the request, send "True"')
    if selector == "True":
        selector = True
    else:
        selector = False
    if not selector:
        try:
            name, host, port = prepare_connect()
            requests.post('http://127.0.0.1:8000/send_request/', data={"name": str(name), "ip": host, "port": port})
            connect(host, port, name, server=False, selector=False)
        except SystemExit:
            os._exit(1)

    elif selector:
        coll_name = input('Please write name of the collocutor here: ')
        try:
            req = requests.get('http://127.0.0.1:8000/requests/').json()
            if coll_name not in req:
                print("The collocutor is not on the waiting list")
                os._exit(1)
            access = req[coll_name]  # парсим ip  и порт по указанному имени
            requests.delete('http://127.0.0.1:8000/delete_data/', data={"name": coll_name})
            # после полученния данных для соединения сразу же удаляем запись по имени юзера, инициировавшего соединение
            server = (access.split(':')[0], int(access.split(':')[1]))
            name, host, port = prepare_connect()
            if name == '':
                name = 'Guest' + str(randint(1000, 9999))
                print('Your name is:' + name)
            connect(host, port, name, server, selector)
        except SystemExit:
            os._exit(1)


if __name__ == '__main__':
    run()
