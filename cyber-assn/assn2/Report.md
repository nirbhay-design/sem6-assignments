## Nirbhay Sharma (B19CSE114)
## cyber-security - lab-2
## Topic: Hands on with ssh commands
---

### how to connect to iitj remote server using ssh from terminal
---

1. first connect to the iitj forticlient vpn (if outside campus)

![iitjvpn](https://github.com/nirbhay-design/markdown-images-pdf-repo/blob/master/cyber-lab2/Capture1.PNG?raw=true)

2. then connect to the server using the following command: *ssh u108@172.25.0.42* then enter password
as shown below

![ssh-connect](https://github.com/nirbhay-design/markdown-images-pdf-repo/blob/master/cyber-lab2/Capture2.PNG?raw=true)

### how to transfer files from your local system to remote server using scp command
---

1. first select a file to transfer as shown below

![files-show](https://github.com/nirbhay-design/markdown-images-pdf-repo/blob/master/cyber-lab2/Capture3.PNG?raw=true)

2. then send the file to remote server using scp command shown below

![file-scp-transfer](https://github.com/nirbhay-design/markdown-images-pdf-repo/blob/master/cyber-lab2/Capture4.PNG?raw=true)

3. you can see the file on remote server as shown below

![file-remote-server](https://github.com/nirbhay-design/markdown-images-pdf-repo/blob/master/cyber-lab2/Capture5.PNG?raw=true)

### how to transfer files from remote server to local system using scp
---

1. type the following command to transfer from remote to local server

    we can see that file is transferred 100% from remote to local system

![remote-to-local](https://github.com/nirbhay-design/markdown-images-pdf-repo/blob/master/cyber-lab2/Capture6.PNG?raw=true)
    
### how to connect to jupyter notebook using ssh tunneling
---

1. first launch jupyter command on remote server as shown below

![launch-jupyter](https://github.com/nirbhay-design/markdown-images-pdf-repo/blob/master/cyber-lab2/Capture7.PNG?raw=true)

2. then we get the link *http://172.25.0.42:30359* but it is not working in the local machine so use ssh tunneling to run it on a localhost with some localhost using the following command

![ssh-tunnel](https://github.com/nirbhay-design/markdown-images-pdf-repo/blob/master/cyber-lab2/Capture8.PNG?raw=true)

3. see the jupyter notebook on localhost as shown below

![localhost](https://github.com/nirbhay-design/markdown-images-pdf-repo/blob/master/cyber-lab2/Capture9.PNG?raw=true)

4. after the work is over close the remote server as shown in the following figure

![exit](https://github.com/nirbhay-design/markdown-images-pdf-repo/blob/master/cyber-lab2/Capture10.PNG?raw=true)


## learnings from the above hands-on
---
1. how to use ssh to connect to any remote server
2. transfer files using scp from remote to localhost and from localhost to remote server
3. launch jupyter notebook using the concept of ssh tunneling 
