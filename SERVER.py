
from time import sleep
from sys import getsizeof
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 1024))
print('Server is running...')
s.listen(5)

while True:
    clt, adr = s.accept()
    print(f'Connection to {adr} established and shant is awesome')
    r = clt.recv(512)
    if r == bytes.fromhex('F000001400'):
        clt.send(bytes.fromhex('deadbeef'))

clt.close()