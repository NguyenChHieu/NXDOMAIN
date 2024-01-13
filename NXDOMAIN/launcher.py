"""
Write code for your launcher here.

You may import library modules allowed by the specs, as well as your own other modules.
"""
from sys import argv
from pathlib import Path
import random


def check_valid_port(port):
    try:
        port_int = int(port)
        if 1024 <= port_int <= 65535:
            return port_int
        return False

    except ValueError:
        return False


def check_valid_domain(domain, option):
    valid_chars = "abcdefghijklmnopqrstuvwxyz" + "ABCDEFGHIJKLMNOPQRSTUVWXYZ" + "1234567890"
    valid_and_hyphen = valid_chars + "-"
    valid_and_dot = valid_and_hyphen + "."

    domain_parts = domain.lower().rsplit(".", 2)

    if option == "all":
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

    if option == "full" or option == "all":
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


def validate_master(master_file_path):
    try:
        # extract the master content
        with open(master_file_path, 'r') as f:
            lines = f.readlines()

        # extract the master port
        master_port = lines[0].strip()
        if not check_valid_port(master_port):
            print("INVALID MASTER")
            exit()

        # extract the domains and their ports
        records = {}
        for line in lines[1:]:
            domain, port_domain = line.strip().split(',')
            # check valid full domain
            if not check_valid_domain(domain, "full") or \
                not check_valid_port(port_domain) or \
                    (domain in records and records[domain] != port_domain):  # check if there are contradicting records
                print("INVALID MASTER")
                exit()

            # else, save the pairs
            records[domain] = port_domain
        return records, master_port

    # if line 87 unpackable (no "," or not enough parts)
    except ValueError:
        print("INVALID MASTER")
        exit()
    # handle dir not exist, invalid dir perms
    except OSError:
        print("INVALID MASTER")
        exit()


def get_all_ports(records):
    all_ports = []
    for ports in records.values():
        if ports not in all_ports:
            all_ports.append(ports)
    return all_ports


def generate_random_port(ports):
    while True:
        port = random.randint(1024, 65535)
        if port not in ports:
            ports.append(port)
            break
    return port, ports


def root_file_data(records, master_port):
    # get all ports from master file
    all_ports = get_all_ports(records)

    # generate a random root port (no duplication, but can be the same as master port)
    random_root_port, all_ports = generate_random_port(all_ports)
    if random_root_port != master_port:
        all_ports.append(master_port)

    root = {}
    for full_domain, correspond_port in records.items():
        domain_parts = full_domain.strip().rsplit(".", 2)
        tld = domain_parts[-1]
        if tld not in root:
            new_port, all_ports = generate_random_port(all_ports)
            root[tld] = new_port
            all_ports.append(new_port)

    return root, random_root_port, all_ports


def tld_file_data(root_data, records, ports):
    tld_files = {}
    for tld, root_port in root_data.items():
        single_tld_file = {}
        for full_domain, full_port in records.items():
            domain_parts = full_domain.strip().rsplit(".", 2)
            auth_domain = '.'.join(domain_parts[-2:])
            if auth_domain.endswith(tld):  # check if the auth_domain is under this TLD
                if auth_domain not in single_tld_file:
                    new_port, ports = generate_random_port(ports)  # new port for the auth_domain
                    single_tld_file[auth_domain] = new_port  # store the auth_domain and its port

            tld_files[root_port] = single_tld_file

    return tld_files, ports


def auth_file_data(tld_data, records):
    auth_files = {}
    all_dicts = []

    # get auth domains from the previous tld_data
    for tld_port, tld_dictionary in tld_data.items():
        all_dicts.append(tld_dictionary)

    # get the auth domain and ports
    for dictionary in all_dicts:
        for auth_domain, header_port in dictionary.items():
            # deal with each "file" - directory separately
            single_auth_file = {}
            for full_domain, full_port in records.items():
                # distribute the full port into its file
                if full_domain.endswith(auth_domain):
                    if full_domain not in single_auth_file:
                        single_auth_file[full_domain] = full_port

                auth_files[header_port] = single_auth_file

    return auth_files


def write_single_files(directory, records, file_type, header_port=None):

    dir_path = Path(directory)
    try:
        # check if the path passed in exists and is a directory
        if dir_path.exists() and dir_path.is_dir():
            dir_path.mkdir(parents=True, exist_ok=True)

            # write root data
            if file_type == "root":
                str_out = f"{header_port}\n"
                for tld, port in records.items():
                    str_out += f"{tld},{port}\n"
                file_name = "root.conf"
                file_path = dir_path / file_name

                with file_path.open('w') as f:
                    f.write(str_out)

            # tlds/auths
            elif file_type == "tld":
                i = 1
                for port_header, tld_dictionary in records.items():
                    str_out = f"{port_header}\n"
                    for auth, port in tld_dictionary.items():
                        str_out += f"{auth},{port}\n"
                    i += 1
                    file_name = f"tld{i}.conf"
                    file_path = dir_path / file_name

                    with file_path.open('w') as f:
                        f.write(str_out)

            elif file_type == "auth":
                k = 1
                for port_header, auth_dictionary in records.items():
                    str_out = f"{port_header}\n"
                    for full, port in auth_dictionary.items():
                        str_out += f"{full},{port}\n"
                    k += 1
                    file_name = f"auth{k}.conf"
                    file_path = dir_path / file_name

                    with file_path.open('w') as f:
                        f.write(str_out)
        else:
            print("NON-WRITABLE SINGLE DIR")
            exit()
    # dir not writable
    except OSError:
        print("NON-WRITABLE SINGLE DIR")
        exit()


def main(args: list[str]) -> None:

    if len(args) != 2:
        print("INVALID ARGUMENTS")
        exit()

    master_file_path, single_files_dir = args
    records, master_port = validate_master(master_file_path)

    root_file, root_port, all_ports = root_file_data(records, master_port)
    write_single_files(single_files_dir, root_file, "root", root_port)

    tld_files, ports = tld_file_data(root_file, records, all_ports)
    write_single_files(single_files_dir, tld_files, "tld")

    auth_files = auth_file_data(tld_files, records)
    write_single_files(single_files_dir, auth_files, "auth")


if __name__ == "__main__":
    main(argv[1:])