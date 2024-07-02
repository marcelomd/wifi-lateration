# Wifi based indoor positioning system

This project was developed for a startup around 2014-2015. The product was an indoor positioning system that used a few wifi routers/access points to sniff wifi trafic and try to calculate the positions of devices such as phones and tablets. They marketed this to shopping malls and department stores as a tool to analyze customer behavior and foot trafic. 

It's been 10 years and I don't remember much, but I wanted to share this anyway. I finally got around waiving the NDA.

This was a very interesting project, that married several different disciplines, such as RF protocols, networking, embedded systems, backend systems and number crunching.

The general idea was to run a custom sniffer program into the access points. The sniffer detected every single wifi packet around it and recorded the emmiting device's MAC address and its RSSI, the signal strength. Every few seconds we would send a report to a backend server. The backend server generated some quick reports and eventually we would run a batch process that calculated/estimated the devices' position.

Ultimately, the product was not successful because of the inherent lack of accuracy with this method. Also, around this time smartphones started to randomize their MAC addresses, so the positioning would be incomplete anyway.

I'm publishing this code because of the good memories it brings. I have no idea if it still works. This is provided as is. No guarantees.


# Components

* `patches/`: Random OpenWRT patches to compile the sniffer;
* `common/`: Protobuf serializer used by the sniffer to talk to the backend;
* `public/`: Misc configuration files, install scripts for the AP, watchdog cron job;
* `sniff7/`: The actual sniffer;
* `localtracking/`: This is the backend that received the device sightings and generated a few reports;


# Sniffer:

This is a C application that ran on OpenWRT router/access points. The specific device we used was a small Meraki Mesh AP. This device ran a `custom.sh` script on boot. We would use that to install and update our sniffer. 

The sniffer ran 2 threads: the sniffer proper and a reporter.
* The sniffer thread created a monitor pcap interface with a filter that captured any wifi packets detected on the main wifi interface. For each packet we inspected its radiotap header and extracted the device's MAC address and RSSI. This info was written to a circular buffer to be picked up by the reporter thread;
* The reporter thread gathered all the reports from the circular buffer and prepared a packet using protobuf. This was sent to a backend server via HTTP.

# Localtracking

This was actually the first backend I wrote. It's a very simple Python 2/Flask app. It ran on AWS's Elastic Beanstalk. A small instance was enough for servicing several access points. The main idea was to validate the received data and throw it into a queue. A worker process read this queue and inserted the data into the DB. This backend also generated a few simple reports. The actual lateration calculation came later.
