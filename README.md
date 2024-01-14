# NXDOMAIN
NXDOMAIN is a group of 4 small programs that I've created to test with network-related knowledge during my first Uni year.
Consists of: A simple TCP-like server (server.py), a resolver (recursor.py) , a verifier (verifier.py) validates the equivalency of configurations.
and a launcher (launcher.py) which generates DNS server configurations.

An IP address is given to some device on the Internet, and that address is necessary to find the
appropriate Internet device - like a street address is used to find a particular home. **Analogously, a
port can identify a simplified DNS server in these programs**

**1) Recursor Behaviours**

To start the recursor program, the user needs to supply the port of the root nameserver as the
first command-line argument, and the time-out in second as the second argument to the
recursor.

_python3 recursor.py root_port timeout_

When the recursor successfully connects to the root server, it awaits the user to input a domain.
The user will input a hostname to query and end the line by entering a "newline" character \n ,
e.g., by pressing "Enter" on the keyboard.

Then the recursor validates the formation of the domain. If the hostname is invalid, the program
outputs INVALID on the standard output. Otherwise, it starts resolving the domain in six steps:

1. The recursor queries a DNS root nameserver . which is known to it as a command-line
argument. For example, the port assigned to the root is 1026 . When the user is looking up
for alice.bob.carol.dan.eve , the recursor sends eve\n to the root server over TCP at the
port 1026.

2. The root server then responds to the recursor with the port of the TLD DNS server. When
looking up for alice.bob.carol.dan.eve , the response from the root is a port owned by
the eve TLD nameserver. E.g., the recursor receives 1028\n from the root.

3. The recursor then makes a request to the eve TLD by sending dan.eve\n to port 1028
over TCP.

4. The eve TLD server then responds with the port of the authoritative nameserver dan.eve .
E.g., the recursor receives 1030\n from eve .

5. The recursor sends a query to the authoritative nameserver dan.eve by sending
alice.bob.carol.dan.eve\n to port 1030 over TCP.

6. The port for alice.bob.carol.dan.eve is then returned to the recursor from the
nameserver dan.eve over TCP. E.g., the recursor receives 1080\n from dan.eve .


**2) Server Behaviours**

Note that the "server" in this section can be any of the servers described above. That is, the
simplified DNS servers are the same program, despite they may depend on different
configurations.

To start the server program, the user needs to supply a file path of the server's "single"
configuration file as the first command-line argument to the server.

Except for the first line, each line of the server configuration file is a record. Each record consists a
domain or a partial-domain and a port identifier, delimited by comma. The first line of the
configuration contains the port number that the server occupies.

**3) Launcher Behaviours**

The launcher can break down a "master" DNS configuration to a collection of "single" server
configuration files.

A "master" configuration should be equivalent to the collection of "single" configurations that the
launcher generates from the "master".

Syntactically, a "master" configuration is a special kind of "single" configuration which does not
permit any record including a partial-domain.

**4) Verifier Behaviours**

The verifier program can compare a "master" file and a collection of "single" files, and output
whether they are exactly equivalent.

To start the verifier program, the user needs to supply the file path of a "master" configuration file
as the first command-line argument, and the directory path that contains a collection of "single"
configuration files as the second command-line argument.
