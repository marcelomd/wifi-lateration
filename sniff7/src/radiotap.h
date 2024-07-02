/*
 * radiotap.h
 */

#ifndef __RADIOTAP_H
#define __RADIOTAP_H

#include <stdint.h>

/* Extracts the RSSI reading from a Radiotap header.
 * *packet: Pointer to start of packet.
 * length:  Packet size.
 * *signal: RSSI value read from packet.
 * return:  Radiotap header size on success. Negative error code on error.
 */
int radiotap_get_signal(const uint8_t* packet, int length, int8_t* signal);

#endif // __RADIOTAP_H

