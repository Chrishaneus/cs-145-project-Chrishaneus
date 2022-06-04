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

This project was developed using python, the necessary libraries/modules used are the following:
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
<p align="right">(<a href="#top">back to top</a>)</p>

<!-- Prerequisites -->
## Prerequisites
<p align="right">(<a href="#top">back to top</a>)</p>

<!-- Installation -->
## Installation
<p align="right">(<a href="#top">back to top</a>)</p>

<!-- Usage -->
## Usage
