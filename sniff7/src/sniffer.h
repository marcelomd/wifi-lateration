/*
 * sniffer.h
 */

#ifndef __SNIFFER_H
#define __SNIFFER_H

/* Initializes sniffer objects.
 * return:  0 on success. Error code on error.
 */
int sniffer_init(void);

/* Run sniffer thread.
 * return:  0 on success. Error code on error;
 *          contents of *thread are undefined.
 */
int sniffer_start(void);

/* TODO: Closes sniffer thread and frees resources.
 */
void sniffer_stop(void);

#endif // __SNIFFER_H
