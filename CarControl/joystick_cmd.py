import socket


class Joystick:
    def __init__(self):
        self.state = '00'
        self.speed = 1500
        self.angle = 90

    def inc_speed(self):
        if self.speed != 1200:
            self.speed -= 10

    def dec_speed(self):
        if self.speed != 1700:
            self.speed += 10

    def left(self):
        if self.angle != 110:
            self.angle += 5

    def right(self):
        if self.angle != 70:
            self.angle -= 5

    def reset(self):
        self.angle = 90
        self.speed = 1500

    def center(self):
        self.angle = 90

    def stop(self):
        self.angle = 90
        self.speed = 1500
        self.state = '00'

    def send(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('172.24.1.1', 1080)
        try:
            sock.connect(server_address)
            message = '{}/{}/{}'.format(self.state, self.speed, self.angle)
            print(message)
            sock.sendall(message.encode())
        except OSError:
            print('Car not found')
            exit(1)
        finally:
            print('closing socket')
            sock.close()
            if self.state == '00':
                exit(0)
