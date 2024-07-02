/*
 * config.h
 */

#ifndef __CONFIG_H
#define __CONFIG_H

// Config object.
struct config_t {
    unsigned char mac[6];       // This device's MAC address.

    char* base_interface;       // Interface to capture WIFI packets from.
    char* capture_interface;    // Monitor interface over capture interface.
    char* capture_filter;       // Filter expression.
    int capture_snap;           // How many bytes to capture, per packet.

    int buffer_size;            // Packet buffer size.

    int report_interval;        // Seconds to wait between reports.
    int report_server_timeout;  // Seconds to give up on reporting.
    char* report_server;        // Server URL.
    int trace_level;            // Logging/trace level.
                                // Print everything below this.
    int test_mode;              // Test mode.
};

extern struct config_t Config;  // Global Config Object.

/* Initializes this device's configuration.
 * *filename:   File containing configurations.
 * return:  0 on success. Error code otherwise.
 */
int config_init(char* filename);

#endif // __CONFIG_H
