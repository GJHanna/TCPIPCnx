import binascii
from argparse import ArgumentParser
import socket

# Create command-line arguments 
# ip is a must while port is optional with a default value of 6653
# Usage: in the cmd run Python run one of the following
# 'python CLIENT.py 127.0.0.1' <- IP=127.0.0.1, Port=6653
# 'python CLIENT.py 127.0.0.1 653' <- IP=127.0.0.1, Port=653
parser = ArgumentParser()
parser.add_argument('ip', 
                    help='IP Address')
parser.add_argument('port', 
                    nargs='?', 
                    type=int, 
                    default=6653, 
                    help='Port number')

class PortNumberError(Exception):
    pass

class CLIENT(object):
    def __init__(self, ip, port):
        try:
            i = ip.split('.') # 0.0.0.0 becomes an array: [0, 0, 0, 0]

            # Validate IP address
            if (len(i) != 4):
                raise ValueError
            for num in i:
                if (int(num) < 0 or int(num) > 255):
                    raise ValueError
                
            # Validate port number 
            if (port < 0 or port > 65535):
                raise PortNumberError
        except ValueError:
            exit('Invalid IP address format. IP address should be between \
                0.0.0.0 and 255.255.255.255')
        except PortNumberError:
            exit('Invalid port number. Port number should be from 0 to 65535.')
        except Exception:
            exit('IP address should be between 0.0.0.0 and 255.255.255.255. \
                Port number should be from 0 to 65535')
        finally:
            self.__host = ip
            self.__port = port
            self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__sock.settimeout(5)
    
    def connect(self):
        try:
            self.__sock.connect((self.__host, self.__port)) # Connect to IP
            print('Connected to {} through port {}'.format(self.__host,
                self.__port))
        except ConnectionRefusedError:
            exit('Connection refused.')
        except socket.timeout:
            exit('Connection timeout')
        except ConnectionError:
            exit('Connection unreachable.')

    def send(self):
        try:
            # Send data to server from Hex to bytes
            data = 'F000001400'
            self.__sock.send(bytes.fromhex(data))
        except ConnectionRefusedError:
            exit('Connection refused.')

    def receive(self):
        # Received data from server with buffer of 512
        bytes_recvd = self.__sock.recv(1024)
        
        if (bytes_recvd == b''):
            raise ValueError('No data received')
        msb = bytes_recvd[0]
        lsb = bytes_recvd[1]
        val = msb<<8|lsb
        print(val)
        return bytes_recvd 

if __name__=='__main__':
    args = parser.parse_args()
    cnx = CLIENT(args.ip, args.port)
    cnx.connect()
    cnx.send()
    cnx.receive()