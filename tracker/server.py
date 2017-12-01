import socket

s = socket.socket()
host = socket.gethostname()
print(host)
port = 1247
s.bind((host, port))
s.listen(5)
c, addr = s.accept()
print("Connection accepted from " + repr(addr[1]))
c.send("Server approved connection\n".encode())

while True:
    message = str(c.recv(1026))
    print(repr(addr[1]) + ": " + message)
    if message == 'q':
        c.close()
        break
