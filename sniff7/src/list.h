/*
 * list.h
 */

#ifndef __LIST_H
#define __LIST_H

#include <pthread.h>
#include "entry.h"

// List object.
typedef struct {
    entry_t* buffer;        // Buffer containing entries.
    int size;               // Buffer size.
    volatile int counter;   // Next empty entry, contains number of entries.
    pthread_mutex_t lock;   // List lock.
} list_t;

extern list_t List;

/* Initializes List object.
 * return:  0 on success. Error code on error.
 */
int list_init(void);

/* Puts entry into list. If we're putting an entry with a MAC
 * that's already present on list, update its RSSI value.
 * *entry:  Entry object.
 * return:  0 on success. -1 if list is full.
 */
int list_write(entry_t* entry);

/* Pops entry from list.
 * *entry:  Entry object.
 * return:  0 on success. -1 if list is empty (*entry is not touched).
 */
int list_read(entry_t* entry);

/* Empties list.
 */
void list_clear(void);

/* Lock list.
 */
#define list_lock() do { pthread_mutex_lock(&List.lock); } while(0);

/* Unlock list.
 */
#define list_unlock() do { pthread_mutex_unlock(&List.lock); } while(0);

#endif // __LIST_H
