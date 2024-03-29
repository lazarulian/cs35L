# The Internet

## Table of Contents

- [The Internet](#the-internet)
  - [Table of Contents](#table-of-contents)
  - [Client-Server Computing](#client-server-computing)
  - [Alternatives to the Client-Server Model](#alternatives-to-the-client-server-model)
  - [Performance and Correctness Issues](#performance-and-correctness-issues)
    - [Traditional programming performance metrics](#traditional-programming-performance-metrics)
    - [Networking performance metrics](#networking-performance-metrics)
  - [Task Networking Styles](#task-networking-styles)
    - [Circuit Switching](#circuit-switching)
    - [Packet Switching](#packet-switching)
      - [Benefits of Packets](#benefits-of-packets)
      - [Problems with Packet Switching](#problems-with-packet-switching)
  - [Internet Protocol Suite (TCP/IP)](#internet-protocol-suite-tcpip)
    - [Link Layer](#link-layer)
    - [Internet Layer](#internet-layer)
      - [IPv4](#ipv4)
      - [IPv6](#ipv6)
    - [UDP (User Datagram Protocol)](#udp-user-datagram-protocol)
  - [Transport Layer](#transport-layer)
    - [TCP (Transmission Control Protocol)](#tcp-transmission-control-protocol)
  - [Application Layer](#application-layer)
    - [RTP (Realtime Transmission Protocol)](#rtp-realtime-transmission-protocol)
    - [HTTP (HyperText Transfer Protocol)](#http-hypertext-transfer-protocol)
  - [Variants of HTTP](#variants-of-http)
    - [**HTTPS (HTTP Secure)**](#https-http-secure)
    - [**HTTP/1.1**](#http11)
    - [**HTTP/2**](#http2)
    - [**HTTP/3**](#http3)
  - [Data Languages](#data-languages)
    - [SGML (Standard General Markup Language)](#sgml-standard-general-markup-language)
    - [`telnet` Aside](#telnet-aside)

## Client-Server Computing

The Client-Server model, where many browser instances can interact with a single web server, which in turn may be connected to some database:

```
C                     S
+---------+         +------------+
| browser | <-----> | web server |
+---------+         +------+-----+
C                    ^     |
+---------+          |  +--+--+
| browser | <--------+  | DB  |
+---------+             +-----+
```

&nbsp;
&nbsp;
&nbsp;

## Alternatives to the Client-Server Model

- **Single computer** (CS 31 assignments, where the logistics of networking, OS, etc. were abstracted away).

- **Peer-to-peer (P2P)**: Decentralized approach. If a peer doesn't have a resource, the request is redirected to another resource.
  - The main advantage of this is that it is more fault-tolerant: a single peer going down doesn't bring the system down.
  - The downside is that it is more involved to maintain a consistent state across every peer.
  - This is in contrast to the less fault-tolerant but more state-consistent client-server model.
- **Primary secondary**: One primary machine that serves as the "overseer" - it keeps track of how the application is split up among numerous secondary servers.
  - The secondary servers receive a small "subproblem" of the application from the primary server and return any results.

&nbsp;
&nbsp;
&nbsp;

## Performance and Correctness Issues

### Traditional programming performance metrics

---

- CPU time: how many CPU instructions executed (roughly proportional to the amount of energy consumed)
- Real time: amount of human time elapsed
- RAM
- I/O

### Networking performance metrics

---

- **Throughput**: Number of client requests per second that the system can handle (assuming individual requests and responses are reasonably small and approximately equally sized); bigger is better.
- **Latency**: Delay between a request to the server and the response back from the server; smaller is better.

To improve **throughput**:

- ➕ You can perform actions "out of order" (compared to "request order").
- ➕ You can perform actions _in parallel_.
- ➖ This can cause out-of-order execution, which can "mis-order" transactions.

To improve **latency**:

- ➕ You can use **caching** to speed up responses.
- ➖ This can cause **stale caches**, which requires **cache validation** to fix, which could be an expensive operation.

&nbsp;
&nbsp;
&nbsp;

## Task Networking Styles

### Circuit Switching

---

- System is connected to the nearest central office, which can connect to other central offices. In the end, you get a path between the one computer to the other.
  - you have temporary ownership of a wire during the transaction as long as the network stays alive

### Packet Switching

---

- **Packet Switching** is basically connected to a little computer that breaks the signal into a bunch of small messages called **packets**
- Each packet is sent to a local **router** that sends the packets along the network to the destination
- Each packet travels independently and possible along different paths, and they do so very quickly, so it does not back up the network
  - this is a more robust network that owuld allow for one of the centers to go down but the requests to still go through
- Sold to Department of Defense as a reliable way to communicate in the event of nuclear war because of its ability to _reroute_ in the event of an office goes down, which gives it an edge over traditional **circuit switching**.
- Packet switching is a best effort transmission/no guarantees (circuit-switching is a _guarantee_ between the two machines).

#### Benefits of Packets

---

- Packets allow for data to be transmitted efficiently and reliably accross a network
- Smaller packet sizes also allow for error-checking mechanisms to detect errors efficiently at a smaller scale for anything that might go wrong in the transmission
- packets control their routing information

#### Problems with Packet Switching

---

- Packets can be lost - if some router along the way gets overloaded, some packets may be discarded
- Packets can be received out of order
- Packets can be duplicated via a mechanism called **bridges**
- All routing decisions are local to the individual routers, so packets may be directed into a loop
- Packets can be corrupted or stolen

&nbsp;
&nbsp;
&nbsp;

## Internet Protocol Suite (TCP/IP)

- A **protocol** is simply a set of rules. This particular set of rules forms the foundation of the Internet.
- Basic idea: **layering**. Protocols are built on top of each other, with each layer abstracting and extending the one below it:

```
                          End user
                            |
+-----------------------+   |
|   Application Layer   | Applications
+-----------------------+   |
|    Transport Layer    | Data channels
+-----------------------+   |
|    Internet Layer     | Packets
+-----------------------+   |
|      Link Layer       | Bits and bytes
+-----------------------+   |
                            |
                          Hardware
```

### Link Layer

---

- **Point-to-point**
- The bits and bytes you send on a single link from one node to another (no routers in between).
  - Very hardware oriented. Each technology used has its own link layer protocol.
  - there is no network protocol because it is just point a to point be transmission

### Internet Layer

---

- **Packets**
- Software almost never operate directly at this level because it is too low level.
  - there is a network with a set of non-adjacent nodes
  - primary protocols are the IP Protocols (IPV4 and IPV6)

#### IPv4

---

- Involves packet connection.
- We are running out of IPv4 addresses because they are limited in the number there can be regarding IP addresses
- A packet is just a sequence of bytes. The **payload** is prefixed by a **header** that stores **metadata** like:
  - Length.
  - Protocol number (to support any protocol that ends up being built atop IP) tells you the _type_ of packet that's being transported so algorithms can determine their priority. For example, a single video frame is much less important than part of a image file.
  - Source IP address (a 32-bit number often expressed in Base 256).
  - Destination IP address (ibid).
  - A **checksum** (16-bit) to check if there are any errors within the transmission
    - This does not necessarily mean that the packet will not be corrupted, as the checksum can also get corrupted.
    - The checksum merely ensures that the header is not corrupted, not the payload data of the packet
  - **A time-to-live (TTL)** field (8-bit "hop count" that keeps track of how many routers it goes through; packets with abnormally high TTL values get dropped to prevent packet loops).
- When routers receive packets, they look at the header, especially the destination address, to determine what to do with it.

#### IPv6

---

- 128 bit IP addresses.
- The headers are also longer.
- A superset of IPv4; the 32 bits of IPv4 can be mapped to 32 bits of an IPv6 address, so IPv4 users can communicate with IPv6 users. The converse is not as simple but made possible with complicated translation techniques.
- Less efficient because the extra length is overhead for the link layer

### UDP (User Datagram Protocol)

---

- Designed as a thin layer over IP, but still at the Internet layer.
- You use UDP if your application sends single short messages over the Internet without much care if it is lost, duplicated, etc.
  - Intended for apps that _want_ to deal with packets.

&nbsp;
&nbsp;
&nbsp;

## Transport Layer

- **Data channels.** Large data _streams_ (TB of data) that cannot be individual packets
  - This layer oversees how a _stream of packets_ is transmitted
  - has a semblance of order that tries to replicate what we had with circuit switching with packets

### TCP (Transmission Control Protocol)

---

- Looks like a _stream of data_ that

  - Is reliable (via **acknowledgments**)
    - comes at the cost of latency
  - Have **sequence numbers** for packets (dividing streams into ordered packets)
    - Streams are logically independent, the loss of one stream will stall the rest of the streams in the ordering
  - Is ordered (the recipient reassembles the packets that may be out of order in the lower layers)
  - Is **end-to-end error-checked**.
    - For more reliable delivery, higher-layer protocols such as TCP are used, which provide additional error detection and correction mechanisms, such as retransmission of lost or corrupted packets.

- The protocol has
  - Flow control; sends packets at the correct rate to not overload the network (user prevention)
  - Retransmission of corrupted packets
  - Reassembly of unordered packets
- A single machine can listen to multiple TCP channels on different **ports**

&nbsp;
&nbsp;
&nbsp;

## Application Layer

- Application a particular protocl for getting a particular application to run
  - how can the client and the server talk to each other?
  - (web, voice, etc)

### RTP (Realtime Transmission Protocol)

---

- Runs atop UDP because TCP is not suited for sending real-time data. TCP would cause **jitter**.
  - real-time transport protocol that is less reliable but real-time streaming

### HTTP (HyperText Transfer Protocol)

---

- Runs atop TCP because reliability is a must - a single misplaced bracket may break an HTML document.

1. The Web, HTTP and its **request-response protocol**:

   - Create a TCP connection (default port 80)
   - Client sends the server a GET request
   - Server responds with the contents of the webpage and closes the connection

2. **HTML (HyperText Markup Language)**: a way to express the contents of a webpage in a machine-independent format.

> The Internet fundamentally is just HTML and HTTP combined together. HTML is like the content of the Internet, HTTP is how it gets around.

&nbsp;
&nbsp;
&nbsp;

## Variants of HTTP

### **HTTPS (HTTP Secure)**

---

- With plain HTTP, every router between the source and destination can see the raw data that is transmitted.
- Always opens connection, gets request, returns webpage, and closes the connection
  - there is overhead due to the constant opening and closing of the connections

```
Informational responses (100 – 199)
Successful responses (200 – 299)
Redirection messages (300 – 399)
Client error responses (400 – 499)
Server error responses (500 – 599)
```

### **HTTP/1.1**

---

- allows for breaking web pages into pieces and keeping the connection open between the client and the server
  - reduced some of the overhead because of the constant opening and closing the connection

### **HTTP/2**

---

Added extra features to HTTP:

1. Header compression
2. Server push (lets the server send a response without a request - realtime data updates)
3. Pipelining (allows the client to send multiple requests so the server can respond in batches, allows more _parallel_ communication instead of having the client wait for a response every single time)
4. Multiplexing (talk to multiple websites over one TCP channel making efficient requests)

   ![Pipelining](https://upload.wikimedia.org/wikipedia/commons/thumb/1/19/HTTP_pipelining2.svg/640px-HTTP_pipelining2.svg.png)

### **HTTP/3**

---

- Now based on UDP instead of TCP (motivated by the increase in voice/video services)
  - Uses new protocol called Quip which is the high speed merger between TCP and RTP
- Uses even more multiplexing (send many connections, receive many back rather than one at a time)
- Avoids jitter by avoiding **head-of-line** blocking delays; allows content after a dropped packet to be delivered
  - this means that if the packet is missing, it will either drop or let the browser decide what to do rather than to wait for the missing packet and stall the rest of the packets behind it

&nbsp;
&nbsp;
&nbsp;

## Data Languages

- HTML is an example of a data language. We also have:

### SGML (Standard General Markup Language)

---

- A markup language for documents (the 1980s).
- A **declarative** (as opposed to an **imperative**) language.
  - **Markup** specifies the structure and attributes of a document.

```HTML
<QUOTE TYPE="example">
  OK <ITALICS>This text</ITALICS> is part of a block quote intended for example.
</QUOTE>
```

- Extensible bracket types allow you to define new features without making breaking changes to the language.
  - `<QUOTE>` is one type of bracket with its closing tag `</QUOTE>`, `<ITALIC>` is another, etc.
- The structure of the document forms a tree structure: the content inside `<ITALICS>` is a child node to `<QUOTE>`.

&nbsp;
&nbsp;

&nbsp;

### `telnet` Aside

---

You can use the `telnet` command to open a 2-way stream where you can send raw HTTP requests. Run `telnet` with the IP address and the port to connect to. THen enter the `GET` command with the resource you want to get and the protocol version to use. Then specify the `Host`:

```console
$ host www.cs.ucla.edu
WWW.cs.ucla.edu has address 164.67.100.182
$ telnet 164.67.100.182 80
Trying 164.67.100.182...
Connected to 164.67.100.182.
Escape character is '^]'.
GET / HTTP/1.1
Host: www.cs.ucla.edu

HTTP/1.1 301 Moved Permanently
Date: Wed, 19 Oct 2022 22:21:10 GMT
Server: Apache
X-Frame-Options: SAMEORIGIN
Location: https://www.cs.ucla.edu/
Content-Length: 232
Content-Type: text/html; charset=iso-8859-1

<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>301 Moved Permanently</title>
</head><body>
<h1>Moved Permanently</h1>
<p>The document has moved <a href="https://www.cs.ucla.edu/">here</a>.</p>
</body></html>
```

- The actual HTML data is prefixed with a response **header**, detailing metadata like the response code, content length, etc.
