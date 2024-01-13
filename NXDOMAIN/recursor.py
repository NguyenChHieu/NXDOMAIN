"""
Write code for your resolver here.

You may import library modules allowed by the specs, as well as your own other modules.
"""
from sys import argv
import socket
import time


# handle case-insensitive
def check_valid_port(args: list):
    try:
        port_int = int(args[0])
        if 1024 <= port_int <= 65535:
            return port_int
        else:
            print("INVALID ARGUMENTS")
            exit()
    except ValueError:
        print("INVALID ARGUMENTS")
        exit()


def check_timeout(args: list):
    try:
        timeout = float(args[1])
        if timeout > 0:
            return timeout
    except ValueError:
        print("INVALID ARGUMENTS")
        exit()


def check_valid_domain(domain):
    valid_chars = "abcdefghijklmnopqrstuvwxyz" + "ABCDEFGHIJKLMNOPQRSTUVWXYZ" + "1234567890"
    valid_and_hyphen = valid_chars + "-"
    valid_and_dot = valid_and_hyphen + "."

    domain_parts = domain.lower().rsplit(".", 2)

    # C.B.A
    if len(domain_parts) == 3:
        # extract
        domain_c, domain_b, domain_a = domain_parts
        if not domain_a or not domain_b or not domain_c:
            return False

        if domain_c[0] == '.' or domain_c[-1] == '.':
            return False

        for char in domain_a:
            if char not in valid_and_hyphen:
                return False

        for char in domain_b:
            if char not in valid_and_hyphen:
                return False

        for char in domain_c:
            if char not in valid_and_dot:
                return False
        return True


def connect_socket(current_port, timeout, elapsed_time):
    try:
        return socket.create_connection(('localhost', current_port), timeout=timeout - elapsed_time)
    except ConnectionRefusedError:
        return None


def get_port(previous_socket):
    received_data = previous_socket.recv(1024).decode().strip()
    try:
        return int(received_data)
    # handle str
    except ValueError:
        raise Exception("InvalidPort")


def update_elapsed_time(start_time):
    return time.time() - start_time


def process_domain_part(port, domain_part, timeout, elapsed_time, start_time, server_type):
    current_socket = connect_socket(port, timeout, elapsed_time)
    if current_socket is None:
        print(f"FAILED TO CONNECT TO {server_type}")
        exit()

    current_socket.sendall((domain_part + "\n").encode())

    # check for timeout after sending but before receiving
    elapsed_time = update_elapsed_time(start_time)
    if elapsed_time >= timeout:
        raise socket.timeout

    return get_port(current_socket)


def main(args: list[str]) -> None:
    if len(args) != 2:
        print("INVALID ARGUMENTS")
        exit()

    root_port = check_valid_port(args)
    timeout = check_timeout(args)

    while True:
        try:
            domain = input()
        except EOFError:
            break

        if not check_valid_domain(domain):
            print("INVALID")
            continue

        start_time = time.time()
        elapsed_time = 0

        try:
            if elapsed_time >= timeout:
                raise socket.timeout

            # connect to root and get TLD port
            tld = domain.split('.')[-1]
            tld_port = process_domain_part(root_port, tld, timeout, elapsed_time, start_time, "ROOT")
            elapsed_time = update_elapsed_time(start_time)

            if elapsed_time >= timeout:
                raise socket.timeout

            # Connect to TLD and get auth port
            auth_domain = '.'.join(domain.split('.')[-2:])
            auth_port = process_domain_part(tld_port, auth_domain, timeout, elapsed_time, start_time, "TLD")
            elapsed_time = update_elapsed_time(start_time)

            if elapsed_time >= timeout:
                raise socket.timeout

            # Connect to auth and get final port
            final_port = process_domain_part(auth_port, domain, timeout, elapsed_time, start_time, "AUTH")

            if elapsed_time >= timeout:
                raise socket.timeout

            print(final_port)

        except socket.timeout:
            print("NXDOMAIN")
        except ConnectionRefusedError:
            print("FAILED TO CONNECT TO ROOT")
            exit()
        except Exception as e:
            if str(e) == "InvalidPort":
                print("NXDOMAIN")


if __name__ == "__main__":
    main(argv[1:])
