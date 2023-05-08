# File Transfer System

## Overview


A quick and secure method of file transfer is becoming increasingly necessary given the current data security concerns. On this front, there have been numerous developments for decades. Hardware-accelerated transfers, like Infiband, are one example of this. Infiband bypasses the operating system by using Remote Direct Memory Access. Although there are many file transfer methods, there isn’t one all-encompassing solution that combines security, speed, and usability. By offering a quick, secure, and simple file transfer application, our project seeks to address all three problems. With the help of our app, you can send files of any size, from anywhere in the world, quickly, and securely. Thanks to cutting-edge features like encryption and password protection. You can completely customize the interface of our app to meet your unique needs. 

In this project, there are two folders named "Client" and "Server". A server is assumed to be the sender and the client is assumed to be the receiver. We have developed and tested this project on a 2020 Macbook Pro using M1 silicon chip. Therefore, all our steps to replicate the environment will be based on this configuration. 

## Server

The server is the user who would like to send the files. Python3 needs to be installed for this project to run. 

1. We first need to create a virtual environment so that this project doesn't have any package issues using the command: <br>
   `
   python3 -m virtualenv venv
   `
2. Once the virtual environment is created, we need to install all the requirements using the command: <br>
`
pip install -r requirements.txt
`

3. Once all the requirements are installed, we can start the server using the command: <br>
`
python server.py
`

Note: The server runs on the localhost. Therefore, inorder for the server to be visible across the network, we have used the systems IP address. You can get the systems IP address using: <br>
`ipconfig` : Windows <br>
`ifconfig` : Mac <br>

Therefore, find the system IP and replace it in the main function of server.py. 

## Client

Since python doesn't support broadcasting the presence, we need to know the servers IP address. Usually, it is same as the server's system IP. Therefore, in the client directory; go to constants > global_constants and replace the host and port IP with the servers IP. 

Once it is done, we need to create the virtual environment if testing on a different machine. If testing it on the same machine, you can use the same virtual environment. 

Therefore, ensure that all the requirements are installed in the virtual environment and run the client side application using the command: <br>
`
python app.py
`

Once it runs, go to the link: <br> 
`http://localhost:5001`
Note: The host and port of the client can be changed at app.py file incase you wish to run it on a different host and port. 

Once the application starts, you would see a login screen that asks for a username and password. You can use one of the two credentials: 

1. Username: test; password: test
2. Username: kaashyap; password: test


After logging in, you can observe that a new directory for the user is created on the server side. For example, if the username is kaashyap, a new directory with the name kaashyap_dir is created. All the files that you would like to share with the client can be placed in this directory. 

On the client side, you can see a terminal window. Using the linux commands like cd, ls, pwd and get, you can get the list of all the files and folders available and you can fetch the required file using the command: <br>
`
get filename.extension
`

## Note

Our overall aim of the project has been ease of use and needing the least user previleges to run this project. Therefore, we have taken these design decisions of having a dedicated folder for each user and not allowing any other commands that require additional previleges to execute resulting in a seamless execution of the application without any other additional previleges. The entire setup time would take around 30 - 45 minutes to replicate the environment. And, the data we got was mostly from within the code that gave us latency and throughput. 
