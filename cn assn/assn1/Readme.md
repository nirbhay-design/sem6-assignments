# **Nirbhay Sharma (B19CSE114)**

# Features

Full client-server functionality is implemented where 2 servers are made, server1 can handle only one client at a time and server2 can handle any number of clients in parallel using multithreading, the language used for implementing the same is PYTHON

# How to build / run the code
**please follow the following steps**

1. Compile the client code using command: *gcc client.c -o client.out*
2. now run the client and server

    **For one client only**
    * run server: python3 server1.py PORT
    * run client: ./client.out 127.0.0.1 PORT

    **For multiple clients**
    * run server: python3 server2.py PORT
    * run client: ./client.out 127.0.0.1 PORT

# Sample test cases
Format for input entered by client: {operand operator operand} in operand field only **Integers** are allowed and not **float**

(testcase1) 2 + 3 = 5

(testcase2) 2 + 3 + 5 = error (as not supported)  

(testcase3) abcd + abcd = error (not operands)

(testcase4) 2 + -3 = error (format is operand operator operand)

(testcase5) 2 - 3 = -1

(testcase6) 24 * 2 = 48

(testcase7) 1024 / 32 = 32



