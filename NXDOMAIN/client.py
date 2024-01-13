from socket import *
import sys


def main() -> None:
    send = int(sys.argv[1])
    receive_flag = int(sys.argv[2])
    client = socket(AF_INET, SOCK_STREAM)
    client.connect(("localhost", 1024))
    if send == 1:
        client.sendall("!EXI".encode())
    if send == 2:
        client.sendall("T\n".encode())
    if send == 3:
        client.sendall("abc\nbcd\n!EXI".encode())

    # receive?
    if receive_flag == 1:
        data = client.recv(1024).decode('utf-8')
        print(data)
    elif receive_flag == 0:
        pass


if __name__ == "__main__":
    main()
