# echo_select.py

from socket import *
import select

def echo_server(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    input = [sock, ]
    print("The echo select program is running !!!")
    while True:
        r, _, _ = select.select(input, [], [])
        for s in r:
            if s == sock:
                client, addr = sock.accept()
                print("Connect from ", addr)
                echo_handler(client)



def echo_handler(client):
    while True:
        data = client.recv(10000)
        if not data:
            break
        client.send(str.encode("Got select...: ") + data)
    print("Connection closed.")

if __name__ == '__main__':
    echo_server(('', 25000))