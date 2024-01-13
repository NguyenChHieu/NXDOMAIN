"""
Write code for your verifier here.
You may import library modules allowed by the specs, as well as your own other modules.
"""
from pathlib import Path
from sys import argv


def check_valid_port(port):
    try:
        port_int = int(port)
        return 1024 <= port_int <= 65535
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


def read_file(file_path):
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
            stripped_lines = []
            for line in lines:
                stripped_lines.append(line.rstrip())
        return stripped_lines
    except FileNotFoundError:
        return "None"


def read_master_file(master_file_path):
    master_path = Path(master_file_path)

    # check if the path exists
    if not master_path.exists():
        print("invalid master")
        exit()

    master_content = read_file(master_file_path)

    # check if files is empty
    if master_content is None:
        print("invalid master")
        exit()

    try:
        files = {}

        # check if the port (first line) is valid
        if not check_valid_port(master_content[0]):
            print("invalid master")
            exit()

        # domain port mappings
        for line in master_content[1:]:
            domain, port_domain = line.split(",")
            # no comma separated
            if "," not in line:
                print("invalid master")
                exit()
            # check valid port
            if not check_valid_port(port_domain):
                print("invalid master")
                exit()
            # check valid domain
            if not check_valid_domain(domain, "full"):
                print("invalid master")
                exit()
            files[domain] = port_domain
    except Exception:
        print("invalid master")
        exit()
    return files


def read_config(path):
    path_to_dir = Path(path)
    data = {}

    # check if it is a directory
    if path_to_dir.is_dir():
        try:
            # loop through the files path in the specified dir
            for file_path in path_to_dir.iterdir():

                # reset the config file and port everytime
                # after saving the previous file to a dict
                single_config_file = {}
                port = ""

                # extract file data and port
                single_file = read_file(file_path)
                port = single_file[0]

                # extract domains and its corresponding port
                for line in single_file[1:]:
                    # no comma separated
                    if "," not in line:
                        print("invalid single")
                        exit()
                    domain, domain_port = line.split(",")
                    # invalid port
                    if not check_valid_port(domain_port):
                        print("invalid single")
                        exit()
                    # invalid domain
                    if not check_valid_domain(domain, "all"):
                        print("invalid single")
                        exit()
                    single_config_file[domain] = domain_port
                # save the config file (dict) to the whole dict
                data[port] = single_config_file
        except FileNotFoundError:
            print("invalid single")
            exit()
        except PermissionError:
            print("singles io error")
            exit()
    else:
        print("singles io error")
        exit()

    return data


def verifier(master_file_data, config_files_data):
    # Extract all TLDs from the master file
    tlds = set()
    for master_domain in master_file_data.keys():
        tld = master_domain.split('.')[-1]
        tlds.add(tld)

    # Locate the root dictionary
    root_dict = None
    # extracting the port and the domain
    for config_port, config_domains in config_files_data.items():
        # comparing the tlds to see if they matched
        if set(config_domains.keys()) == tlds:
            root_dict = config_domains
            break

    if root_dict is None:
        return False

    # Loop through each domain in the master data
    for master_domain, master_port in master_file_data.items():
        domain_parts = master_domain.rsplit('.', 2)

        # ROOT
        root_domain = domain_parts[-1]
        # if the root domains are not sufficient/false -> neq
        if root_domain not in root_dict:
            return False
        # extract the port
        root_port = root_dict[root_domain]

        # TLD
        tld = '.'.join(domain_parts[-2:])
        # corresponding domain or port is not found -> neq
        try:
            if tld not in config_files_data[root_port]:
                return False
        except KeyError:
            return False
        # extract port
        tld_port = config_files_data[root_port][tld]

        # AUTH
        # corresponding domain or port is not found -> neq
        try:
            if master_domain not in config_files_data[tld_port]:
                return False
        except KeyError:
            return False
        # extract port
        auth_port = config_files_data[tld_port][master_domain]

        # if the final port does not match the one in the master -> neq
        if auth_port != master_port:
            return False

    return True


def main(args: list[str]) -> None:
    if len(args) != 2:
        print("invalid arguments")
        exit()
    master_file_data = read_master_file(args[0])
    config_file_data = read_config(args[1])

    if verifier(master_file_data, config_file_data):
        print("eq")
    else:
        print("neq")


if __name__ == "__main__":
    main(argv[1:])
