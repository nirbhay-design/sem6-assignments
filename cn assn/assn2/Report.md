## Nirbhay Sharma (B19CSE114)
## Computer Network - Lab:2 
---

To install the below commands in linux, do 
> sudo apt install net-tools

1. **ifconfig**
    1. if config command is used to configure or display the current network interface information
    2. my system has 2 interface shown below  
    
    ![img](https://github.com/nirbhay-design/markdown-images-pdf-repo/blob/master/cn-assn%20-%202/1.PNG?raw=true)

    3. command to change ip - 
        > sudo ifconfig eth0 172.31.130.177 netmask 255.255.240.0 up
    
    ![igm](https://github.com/nirbhay-design/markdown-images-pdf-repo/blob/master/cn-assn%20-%202/2.PNG?raw=true)

    4. virtual ip address is an address that does not corresponds to the physical network interface
    - command for adding a virtual ip address
        > sudo ifconfig eth0:0 10.0.0.1

        > sudo ifconfig eth0:1 10.0.0.2

        > sudo ifconfig eth0:2 10.0.0.3

    ![img](https://github.com/nirbhay-design/markdown-images-pdf-repo/blob/master/cn-assn%20-%202/3.PNG?raw=true)


2. **route**

    1. route command in Linux is used when you want to work with the network routing table. The command allows us to make manual entries into network routing tables using this command we can delete, change, get a partiuclar route
    2. using the command
   
    ![img](https://github.com/nirbhay-design/markdown-images-pdf-repo/blob/master/cn-assn%20-%202/4.PNG?raw=true)
    
    ![img](https://github.com/nirbhay-design/markdown-images-pdf-repo/blob/master/cn-assn%20-%202/5.PNG?raw=true)

    - from above output we can interpret that if the destination ip is between 172.31.128.0 till Genmask then gateway is * i.e. 0.0.0.0
  
    3. from the above images we can see that thhe packets are forwarding to gateway 172.31.128.1
    4. > sudo ip addr add 192.168.178.201/24 dev eth0

    5. add route 
    
    ![img](https://github.com/nirbhay-design/markdown-images-pdf-repo/blob/master/cn-assn%20-%202/16.PNG?raw=true)

    7. delete route 

    ![img](https://github.com/nirbhay-design/markdown-images-pdf-repo/blob/master/cn-assn%20-%202/17.PNG?raw=true) 


3. **arp**

    1. arp flags are as follows 
       1. C flag - complete entries are marked with C flag
       2. M flag - permanant entries are marked with M flag
       3. P flag - published entries are marked with P flag
    - some of the flags are shown below

    ![images](https://github.com/nirbhay-design/markdown-images-pdf-repo/blob/master/cn-assn%20-%202/15.PNG?raw=true)

    1. No, we cannot use arp to find MAC address of google.com as arp can run only on local networks


4. **arping**
   
   1. it can be used to find hosts on a particular network
   2. we can see the ip using arp list by doing
        > arp -n
   3. > sudo apring 172.24.144.1 
   
   ![img](https://github.com/nirbhay-design/markdown-images-pdf-repo/blob/master/cn-assn%20-%202/6.PNG?raw=true) 

   1. arping is different from ping because ping works at network layer and arping works at link layer
   2. another point is arping can be run only on local system but ping can also run on remote host

5. **netstat**

    - netstat is used to see the status of an ip such as what ports are listening or are already connected or which ports are using tcp / udp etc. it is also used to see routing tables, interface statistics etc.
    
    - we can fire various commands to in netstat such as
    
    ```
    $ netstat -a  (give all the ports)
    $ netstat -at (give all tcp ports)
    $ netstat -au (gives all udp ports)
    $ netstat -l (gives all listening ports)
    $ netstat -lt (gives all listening tcp ports)
    $ netstat -lu (gives all listening udp ports)
    ```

    - some commands are shown below:
  
    ![img](https://github.com/nirbhay-design/markdown-images-pdf-repo/blob/master/cn-assn%20-%202/7.PNG?raw=true)

    ![img](https://github.com/nirbhay-design/markdown-images-pdf-repo/blob/master/cn-assn%20-%202/8.PNG?raw=true)



6. **nslookup** (used to query internet name servers)

    - > nslookup iitj.ac.in

    ![img](https://github.com/nirbhay-design/markdown-images-pdf-repo/blob/master/cn-assn%20-%202/10.PNG?raw=true)

    - > nslookup google.com

    ![img](https://github.com/nirbhay-design/markdown-images-pdf-repo/blob/master/cn-assn%20-%202/11.PNG?raw=true)

    - > nslookup yahoo.com
    
    ![img](https://github.com/nirbhay-design/markdown-images-pdf-repo/blob/master/cn-assn%20-%202/12.PNG?raw=true)

    - the output can be explained in this way like it is showing us the DNS name and address for a paricular ip which are present in our DNS cache

7. **ssh**

    - connecting to iitj remote server 
        > ssh u108@172.25.0.42
    
    ![ssh-connect](https://github.com/nirbhay-design/markdown-images-pdf-repo/blob/master/cyber-lab2/Capture2.PNG?raw=true)

    - keygen

    ![keygen](https://github.com/nirbhay-design/markdown-images-pdf-repo/blob/master/cn-assn%20-%202/9.PNG?raw=true)

    - > scp nirbhay.txt u108@172.25.0.42:
  
    ![file-scp-transfer](https://github.com/nirbhay-design/markdown-images-pdf-repo/blob/master/cyber-lab2/Capture4.PNG?raw=true)

    - > scp u108@172.25.0.42:file1.txt file1.txt 

    ![remote-to-local](https://github.com/nirbhay-design/markdown-images-pdf-repo/blob/master/cyber-lab2/Capture6.PNG?raw=true)

8. **traceroute**
    - It is used to determine the path between two connections, it returns the name and ip of all the routers that occur between two devices
    - examples

    ![img](https://github.com/nirbhay-design/markdown-images-pdf-repo/blob/master/cn-assn%20-%202/13.PNG?raw=true)

    - we can trace packet to iitj.ac.in as follows

    ![traceroute](https://github.com/nirbhay-design/markdown-images-pdf-repo/blob/master/cn-assn%20-%202/14.PNG?raw=true)

    - yes, we can find RTT to using traceroute command, so basically traceroute by default send three packets in one hop and hence it gives three RTT time in ms for each hop

    - Traceroute most commonly uses ICMP echo packets for windows
    - and for linux / mac it uses UDP packets as default