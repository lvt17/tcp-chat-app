### server.socket()
server.socket(***family***, ***type***)
server = socket(***socket.AF_INET***, ***socket.SOCK_STREAM***)

***socket.AF_INET***: 
AF = Address Family; 
INET = Internet Protocol version 4 (IPv4 (eg: 192.168.1.1))

This means the socket use for internet with IPv4 address

***socket.SOCK_STREAM***:
This is TCP protocol, use when the reliablity is needed: chat, file transfer, HTTP,...

## client_socket, addr = server.accept()

