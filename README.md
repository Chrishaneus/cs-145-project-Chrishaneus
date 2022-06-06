<div id="top"></div>

<!-- TITLE -->
<div align="center">
  <h3 align="center">CS 145</h3>
  <h4 align="center">PARAMETER-ADAPTIVE RELIABLE UDP-BASED PROTOCOL</h4>

  <p align="center">
    implementation of the sender side of a protocol, as well as its parameter estimation module or component.
    <br />
    <a href="https://github.com/Chrishaneus/cs-145-project-Chrishaneus"><strong>Explore the docs »</strong></a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About the Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#others">Others</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About the Project
This project was made with accordance to CS 145 2021-2022 requirements as a project. It is an implementation of the sender side of a protocol, as well as its parameter estimation module or component.

The network protocol is a pipelined protocol built on top of UDP. To send the total payload of the sender to the receiver or test server, the protocol’s operation proceeds in three steps.

* Step One: Downloading the Payload
* Step Two: Initiating a Transaction
* Step Three: Sending the Payload or Data

A receiver can only accept payloads of up to a certain size, denoted in ASCII characters. The payload limit would vary from one data (generated in Step One) to the other, and is hidden. The packets sent to the receiver will be placed in a queue - the queue length is finite, would vary from one data (generated in Step One) to the next, and is hidden. The receiver will process the packets in the queue at regular intervals. The length of the interval would vary from one data (generated in Step One) to the next, and is hidden from the sender.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- Built With -->
## Built With
This project was developed using python 3, the necessary libraries/modules used are the following:
* socket    - socket instance and sending/receiving packets
* time      - latency and processing time approximation
* hashlib   - hashing and verification
* sys       - command line inputs and systematic exits
* ipaddress - IP verification
* os        - force exits
* string    - randomizes transaction IDs (server implementation)
* threading - concurrently receive and send ack packets in the queue (server implementation)
* math      - calculations
* random    - randomizes hidden parameters

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- Getting Started -->
## Getting Started
Download/clone this repository and put the folder anywhere in your device. Open your terminal and check your IP address (local) using `ipconfig` (windows) or `ifconfig` (unix) and take note of this address. Create a .txt file and fill it with text (in one line if possible). Then, edit the `server.py` file in line `43` to the path of the created .txt file.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- Prerequisites -->
## Prerequisites
You may install Visual Studio Code for ease of testing. Do note that the steps stated earlier are necessary for locally testing the implementation. Also, follow the <a href="#installation">installation section</a> if you need help with any installation issues.

<p align="right">(<a href="#top">back to top</a>)</p>
<div id="installation"></div>

<!-- Installation -->
## Installation
For the project to work, you need an installation of <a href="https://www.python.org/downloads/">python</a> >= 3.5 in your device. The version that is installed in the AWS instance given was 3.10.4. If any of the aformentioned modules or libraries are not pre-installed with your python installation, you can use the following command in your terminal:

````
pip install <module name>
````

Once all needed modules are installed,  you can now proceed to the <a href="#usage">next</a> section.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- Usage -->
## Usage
__Take note of the following flags for the `sender.py` file:__
* -f denotes the filename of the payload (default value: your id .txt e.g. CS143145.txt)
* -a denotes the IP address of the receiver to be contacted (default value: 10.0.7.141; this is also the IP of the receiver that you will use when developing your project)
* -s denotes the port used by the receiver (default value: 9000; this is also the port of the receiver that you will use when developing your project)
* -c denotes the port used by the sender; this port is assigned per student, given at the same time as the unique ID (default value: your assigned port)
* -i denotes the unique ID; this ID is assigned per student, given at the same time as the port assigned to the student (default value: your id e.g. CS143145)

Note that if these fields are stated in the command line, it would be set to the default value. Also, if ever you entered the flag without any values it would set it to default. If also for whatever reason, there are two flag instances in one command it would get the value for only the first flag.

> Note: the default values are set in the `Parser.py` module.

__For local testing you may do the following:__
1. open two terminal instances (tmux, vscode terminals, etc.) and go the project's directory.
2. take note of your local IP address you got in the <a href="#getting-started">getting started</a> section as well as the .txt file you entered to the server.
3. run the following command in one terminal:
````
python3 server.py
````
4. run the following command in the next terminal:
````
python3 sender.py -f <path-to-txt-file> -a <your-IP-address> -s 9000 -c <port> -i <ID>
````
5. Wait and check the exchanges in the terminal between the client (sender) and server (receiver).

> Note: the local server is defaulted to listen to port `9000`. The server is just suppose to be a replication of the server provided by the handlers of the project.

__For other testing methods:__
1. open a terminal instance and go the project's directory.
2. take note of the fields/flags you need including the file path, IP address of receiver, server port, client port, and ID.
3. run the following command in the terminal:
````
python3 sender.py -f <path-to-txt-file> -a <your-IP-address> -s <server-port> -c <client-port> -i <ID>
````
4. verify through the server (or transaction history) the details of the transaction.

> Note: a log.txt file was also provided to see the latest transaction ID made along with the address of the server.

<!-- Others -->
## Others
the `.pcap` files included in the captures folder. In total there are $6$ tests in the `test_documentation.pcap` file and the first five are in the documentation. Additionally, there are $19$ additional consecutive tests done in the `test_additional.pcap` file. The packets captured when testing the commands (which are also included in the documentation video) is in the `test_commands.pcap` file.
