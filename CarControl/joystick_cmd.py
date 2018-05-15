import socket
import time

n = 1

class Joystick:
    def __init__(self):
        self.state = '00'
        self.speed = 1500
        self.correction = -1
        self.angle = 90 + self.correction
        self.send()

    def inc_speed(self):
        self.speed = min(max(self.speed - 2, 1200), 1400)
        self.speed = 1385

    def dec_speed(self):
        self.speed = max(min(self.speed + 1, 1700), 1600)
        self.speed = 1600

    def left(self):
        self.angle = min(self.angle + 4, 110)
        self.angle = 100

    def right(self):
        self.angle = max(self.angle - 4, 70)
        self.angle = 80

    def reset(self):
        self.angle = 90 + self.correction
        self.speed = 1500

    def center(self):
        self.angle = 90 + self.correction

    def stop(self):
        self.angle = 90
        self.speed = 1500
        self.state = '11'

    def send(self):
        global n
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('172.24.1.1', 1080)
        try:
            sock.connect(server_address)
            message = '{}/{}/{}'.format(self.state, int(self.speed - abs((self.angle - self.correction) * 0.1)), self.angle)
            message = '{}/{}/{}'.format(self.state, self.speed, self.angle)
            print(n, time.time(), message)
            sock.sendall(message.encode())
            n += 1
        except OSError:
            print('Car not found')
            exit(1)
        finally:
            sock.close()
            if self.state == '11':
                exit(0)
