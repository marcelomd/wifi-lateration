# Wifi based indoor positioning system

This project was developed for a startup around 2014-2015. The product was an indoor positioning system that used a few wifi routers/access points/stations to sniff wifi trafic and try to calculate the positions of devices such as phones and tablets. They marketed this to shopping malls and department stores as a tool to analyze customer behavior and foot trafic. IIRC there were a few companies doing it, like Navizon and Euclid.

It's been 10 years and I don't remember much, but I wanted to share this anyway. I finally got around waiving the NDA.

This was a very interesting project, that married several different disciplines, such as RF protocols, networking, embedded systems, backend systems and number crunching.

The general idea was that every device emits wifi packets that can be captured by a set of access points. We know the signal intensity of that packet and, in theory, that number is proportional to the distance between access point and device. With 3+ APs we can use some geometrical method to estimate the device's position relative to the APs.

To do that, in every AP we ran a custom sniffer program. The sniffer detected every single wifi packet around it, recorded the emmiting device's MAC address and its RSSI. Every few seconds we would send a report to a backend server. The backend server generated some quick reports and eventually we would run a batch process that calculated/estimated the devices' position.

Ultimately, the product was not successful because of the inherent lack of accuracy with this method. Also, around this time smartphones started to randomize their MAC addresses, so the positioning would be incomplete anyway.

I'm publishing this code because of the good memories it brings. I have no idea if it still works. This is provided as is. No guarantees.


# Components

* `patches/`: Random OpenWRT patches to compile the sniffer;
* `common/`: Protobuf serializer used by the sniffer to talk to the backend;
* `public/`: Misc configuration files, install scripts for the AP, watchdog cron job;
* `sniff7/`: The actual sniffer;
* `localtracking/`: This is the backend that received the device sightings and generated a few reports;
* `lateration-app/`: This is the backend that does the positioning
* `lateration-lab/`: Series of experiments trying to refine the lateration process


# Sniffer:

This is a C application that ran on OpenWRT router/access points. The specific device we used was a small Meraki Mesh AP. This device ran a `custom.sh` script on boot. We would use that to install and update our sniffer. 

The sniffer ran 2 threads: the sniffer proper and a reporter.
* The sniffer thread created a monitor pcap interface with a filter that captured any wifi packets detected on the main wifi interface. For each packet we inspected its radiotap header and extracted the device's MAC address and RSSI. This info was written to a circular buffer to be picked up by the reporter thread;
* The reporter thread gathered all the reports from the circular buffer and prepared a packet using protobuf. This was sent to a backend server via HTTP.


# Localtracking

This was actually the first backend I wrote. It's a very simple Python 2/Flask app. It ran on AWS's Elastic Beanstalk. A small instance was enough for servicing several access points. The main idea was to validate the received data and throw it into a queue. A worker process read this queue and inserted the data into the DB. This backend also generated a few simple reports. The actual lateration calculation came later.


# Lateration App

I don't remember every detail here, but the process is straightforward. We have a list of nodes, the access points, and we know their positions. The positioning/location is performed by taking a detected device and minimizing the estimated distances to all APs. This was done using scipy and could be done more or less in real time.

In the end wifi turned out to be inaccurate for what we were trying to do, locate people in closed spaces. All kinds of reasons for it. Sometimes a smartphone wouldn't emit packetss. Sometimes an AP wouldn't pick up all packets we knew were there. RSSI gets more inacurate with distance. Sometimes the packets would be detected via a reflection, so the distance would be wildly off.

To minimize that, we used our own nodes, which were fixed, to calibrate some parameters of the equations. We also experimented with different solver methods and norms.


# Lateration Lab

This is just a bunch of random code I wrote to try to get better results.

One promising positioning method was to forget the idea of tracking people's exact positions and simply put them in a sector, like near the store's entrance, cashiers, shoe racks, kids' section, etc. We did a calibration round: we had someone stand at the center of each sector for 5-10 minutes and record all their packets. Then we transformed the average of each sector into a fingerprint. This was used as an input to a binning algorithm, like KNN, to assign sectors to detected devices.