SID: 530382197
Name: Chi Hieu Nguyen

This is the guidance for my testing part =).

+ The testing includes the test of basic server functions, commands, 
server's buffer and error handling.

  + There will be several different folders which will mostly contain the .in, .out 
    and correspondingly to their testing purpose (however for the arguments and
    configuration file testing, we don't need input therefore there won't be .in files)
  +  The actual output will be stored temporarily and will be compared with the .out file.
  +  Before each test, the label will be presented before it runs (example: 1.1)

  + "sample_files" : folder which contain both valid and invalid configuration files.
     + sample.conf: valid config file
     + sample_1.conf: invalid root config file
     + sample_2.conf: invalid port attached to domain in config file
     + sample_3.conf: conflict domain file
  
  + Client.py - program I used to test the server's buffer

  + Note: in run.sh, u can choose to view the report in terminal or in html.

**PART 1: TESTING ARGUMENTS + VALIDATING CONFIG FILE**

  1) TESTING ARGUMENTS - test 1.1
     + Test 1.1 - "too many arguments" 
     Des: too many arguments were passed into server.py
     Output: INVALID ARGUMENTS\n
  
  2) VALIDATING CONFIG - test 1.2 - 1.5
     + Test 1.2 - "config file not found" 
     Des: valid arguments but server.py cannot read the config file. 
     Output: INVALID CONFIGURATION\n

     + Test 1.3 - "invalid root port"
     Des: passed in a valid config file (sample_1.conf) but with invalid root port (9)
     Output: INVALID CONFIGURATION\n

     + Test 1.4 - "invalid domain found"
     Des: passed in a valid config file (sample_2.conf) but with invalid port attached (1000000)
     Output: INVALID CONFIGURATION\n

     + Test 1.5 - "conflict domain"
     Des: passed in a valid config file (sample_3.conf) but there are 2 conflict ports
     + "com,1025
        com,1026"
     Output: INVALID CONFIGURATION\n

**PART 2: TESTING SERVER NORMAL BEHAVIOR**
    + Note: After tested, the server exits.

  1) TESTING VALID DOMAIN
     + Test 2.1.1 - "valid_a"
     + (As long as the domain is in the dictionary, then its resolvable)
       Des: passed in a valid, exist domain name in form :
        + "A" - "com\n" 
        + "B.A" - "google.com\n"
        + "C.B.A" - "www.google.com\n"
       Output: 
       resolve com to 1025
       resolve google.com to 1026
       resolve www.google.com to 1027

  2) TESTING INVALID DOMAIN
     
     + Test 2.1.2 - "valid_nxdomain"
       Des: passed in a valid, non-existent domain "sheesh\n"
       Output: resolve sheesh to NXDOMAIN

     + Test 2.2 - "invalid_a"
       Des: passed in invalid, non-existent domain names in form "A" - "co~m\n" 
       Output: INVALID\n
     
     + Test 2.3 - "invalid_b_a"
       Des: passed in invalid, non-existent domain names in form "B.A" 
     - "go~ogle.com\n" 
        Invalid "B"
     - "google.co~m\n"
        Invalid "A"
       Output: INVALID\n
     
     + Test 2.4 - "invalid_c_b_a"
       Des: passed in invalid, non-existent domain names in form "C.B.A" 
  
     - ".example..google.com\n"
        "." at the start or end of "C"
     
     - ".com." 
        3 domain parts but "C","A" empty
     
     - "ex~ample.google.com\n" 
       "C" invalid
     
     - "example.go~ogle.com\n" 
       "B" invalid
     
     - "example.google.c~om\n" 
       "A" invalid
       Output: INVALID\n
     
**PART 3: TESTING SERVER COMMAND**
    + Note: After tested, the server exits.

  + Test 3.1 - check EXIT function - valid:
    "!EXIT\n"
    Output:
    (nothing)

  + Test 3.2.1 - check !ADD function - valid:
    "!ADD net 1029\n"
    Des: Add valid domain net - port 1029 to the server.
    Output:
    (nothing since the domain saved in server's RAM and not printed out)

  + Test 3.2.2 - check !ADD function - invalid port:
    "!ADD net hi\n"
    Des: Add valid domain net - invalid port "hi" to the server.
    Output:
    (nothing since the server will do nothing base on the specs)

  + Test 3.2.3 - check !ADD function - invalid port:
    "!ADD net 1026\n"
    Des: Add valid domain net - invalid port 1026 (has been used by google.com) 
    to the server.
    Output:
    (nothing since the server will do nothing)

  + Test 3.3 - check !DEL function - valid:
    "!DEL com\n"
    Des: Delete valid domain in server "com\n"
    Output:
    (nothing)

  + Test 3.4 - check invalid command:
    "!HELLOO\n"
    Des: invalid command
    Output: INVALID\n
   
**PART 4: TESTING SERVER BUFFER**
    + Note: After tested, the server exits.
    + Instead of using netcat and cat "input files", I used client.py to send incomplete msgs
    + client.py based on the first cmd line argument to send the msgs to server
    by using sendall, and the second cmd line argument will determine when I want to 
    receive the data sent from the server
    + since im using client.py -> no input files

  + Test 4.1 - check buffer function:
    Send "!EXI" - this will be saved into the buffer and then send "T\n" to exit
  + Explaining the process:
    1) Using client.py, I first send "!EXI" to the server
    2) Next, I use client.py to send "T\n", you will notice a blank line got printed
    out, that is what the client received from the server (in this case nothing was
    received since it's the exit command) then the client exits
    Output: (nothing)
    
  + Test 4.2 - interrupted msgs:
    Send "abc\nbcd\n!EXI" - resolve 2 NXDOMAINs, then store !EXI in the buffer
    Then, send "T\n" -> the uncompleted message become a completed message :"!EXIT\n"
    then exit the server
  + Explaining the process:
    1) Using client.py, I first send "abc\nbcd\n!EXI" to the server then the client received
    2 NXDOMAINs, and !EXI is stored in the buffer as an uncompleted message.
    2) Next, I use client.py to send "T\n" then the server exits
    Output: (nothing)
  + The 2 "NXDOMAIN
           NXDOMAIN"
    is what the server received, and similarly to test 4.1, the server will have a blank
    line after exit.

    Output:
    resolve abc to NXDOMAIN
    resolve bcd to NXDOMAIN

        

