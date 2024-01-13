"""
Write code for your server here.

You may import library modules allowed by the specs, as well as your own other modules.
"""
from sys import argv
import socket


def get_domains_and_ports(arg):
    config_file_path = arg

    # read configuration and handle file error
    try:
        with open(config_file_path, 'r') as f:
            lines = f.readlines()
        # get the port of the server
        port = int(lines[0])

        # check if root port is invalid
        if not check_valid_port(port):
            print("INVALID CONFIGURATION")
            exit()

        domain_mappings = {}
        # extract other domains and their ports
        for line in lines[1:]:
            domain, domain_port = line.strip().split(',')
            domain = domain.lower()

            # check if there are any invalid domains or ports
            if not check_valid_domain(domain) or not check_valid_port(domain_port):
                print("INVALID CONFIGURATION")
                exit()

            # check for contradicting records
            if domain in domain_mappings:
                if domain_mappings[domain] != domain_port:
                    print("INVALID CONFIGURATION")
                    exit()

            domain_mappings[domain] = domain_port
        return port, domain_mappings

    except FileNotFoundError:
        print("INVALID CONFIGURATION")
        exit()


def check_valid_command(components):
    cmd = components[0].strip()

    return ((cmd == "!ADD") and (len(components) == 3)) \
        or ((cmd == "!DEL") and (len(components) == 2)) \
        or ((cmd == "!EXIT") and (len(components) == 1))


# handle case-insensitive
def check_valid_domain(domain):
    valid_chars = "abcdefghijklmnopqrstuvwxyz" + "ABCDEFGHIJKLMNOPQRSTUVWXYZ" + "1234567890"
    valid_and_hyphen = valid_chars + "-"
    valid_and_dot = valid_and_hyphen + "."

    domain_parts = domain.lower().rsplit(".", 2)

    # A
    if len(domain_parts) == 1:
        for char in domain_parts[0]:
            if char not in valid_and_hyphen:
                return False
        return True

    # B.A
    elif len(domain_parts) == 2:
        domain_b, domain_a = domain_parts
        for char in domain_a:
            if char not in valid_and_hyphen:
                return False
        for char in domain_b:
            if char not in valid_and_hyphen:
                return False
        return True

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


def check_valid_port(port):
    try:
        port_int = int(port)
        return 1024 <= port_int <= 65535
    except ValueError:
        return False


# handle case-insensitive
def do_command(cmd, components, dictionary, sockets):
    if cmd == "!ADD":
        domain, port = components[1::]
        domain = domain.lower()
        if (check_valid_domain(domain)) and (check_valid_port(port)) and (port not in dictionary.values()):
            if port not in dictionary.values():
                dictionary[domain] = port
    elif cmd == "!DEL":
        domain = components[1].lower()
        if check_valid_domain(domain):
            del dictionary[domain]
    elif cmd == "!EXIT":
        sockets.close()
        exit()


def get_response(data, dictionary):
    if data in dictionary:
        responses = dictionary[data] + "\n"
    else:
        responses = 'NXDOMAIN\n'

    return responses


def main(args: list[str]):

    # error handling
    if len(args) != 1:
        print("INVALID ARGUMENTS")
        exit()

    # extract from configuration file
    port, domain_map = get_domains_and_ports(args[0])

    # initialize socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # avoid bug
    s.bind(('localhost', port))
    s.listen()

    buffer = ""

    while True:
        conn, addr = s.accept()
        data = conn.recv(1024).decode('utf-8')
        # check "\n" in buffer  ( "abc\ndef\n -> ["abc","def", ""] )
        buffer += data
        if "\n" in buffer:
            messages = buffer.split("\n")

            # check "\n" at the end
            # if true, buffer = ""
            # else, buffer = msg[-1]
            if not messages[-1]:
                buffer = ""
            else:
                buffer = messages[-1]

            # send the data back without missing any
            response_accumulator = ""

            for data in messages[:-1]:
                # check for command function
                if data.startswith("!"):
                    components = data.split()
                    cmd = components[0]

                    if check_valid_command(components):
                        do_command(cmd, components, domain_map, conn)
                    else:
                        print("INVALID")

                # normal domain behaviour
                else:
                    if check_valid_domain(data):
                        response = get_response(data, domain_map)
                        response_accumulator += response
                        print(f"resolve {data} to {response.strip()}")
                    elif not check_valid_domain(data):
                        print("INVALID")
            if response_accumulator:  # Only send if there's something to send
                conn.send(response_accumulator.encode('utf-8'))


if __name__ == "__main__":
    main(argv[1:])
