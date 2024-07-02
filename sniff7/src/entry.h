/*
 * entry.h
 */

#ifndef __ENTRY_H
#define __ENTRY_H

// Entry object.
typedef struct {
    unsigned char mac[6];   // MAC address of device.
    unsigned int timestamp; // Timestamp =)
    short rssi;             // sum of RSSI readings from this mac this second.
    char count;             // How many times this mac was seen
                            // this second.
} entry_t;

#endif // __ENTRY_H
