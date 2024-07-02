/*
 * list.c
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "config.h"
#include "trace.h"
#include "list.h"

/*****************************************************************************/

list_t List; // List of devices seen.

/*****************************************************************************/

int list_init(void)
{
    trace(TRACE_INFO, "List> init!\n");
    List.size = Config.buffer_size; // Test for power of 2
    List.counter = 0; //counter
    List.buffer = calloc(List.size, sizeof(entry_t));
    if (List.buffer == NULL) {
        trace(TRACE_ERROR, "List> buffer error!\n");
        return -1;
    }
    if (pthread_mutex_init(&List.lock,NULL)) {
        trace(TRACE_ERROR, "List> mutex error\n");
        return -1;
    }
    return 0;
}

/*****************************************************************************/

int list_write(entry_t* entry)
{
    int i;
    if (List.counter == List.size)
        return -1;
    for (i = 0; i < List.counter; i++) {
        if (!memcmp(List.buffer[i].mac, entry->mac, 6) &&
                List.buffer[i].timestamp == entry->timestamp) {
            List.buffer[i].rssi += entry->rssi;
            List.buffer[i].count++;
            trace(TRACE_DEBUG, "List> old [%d/%d] %d - %d (%d) %02x%02x%02x%02x%02x%02x\n",
                    i, List.counter,
                    entry->timestamp, List.buffer[i].count, entry->rssi,
                    entry->mac[0],entry->mac[1],entry->mac[2],
                    entry->mac[3],entry->mac[4],entry->mac[5]);
            return 0;
        }
    }
    memcpy(&List.buffer[i], entry, sizeof(entry_t));
    List.buffer[i].count = 1;
    List.counter++;
    trace(TRACE_DEBUG, "List> new [%d/%d] %d - %d (%d) %02x%02x%02x%02x%02x%02x\n",
            i, List.counter,
            entry->timestamp, List.buffer[i].count, entry->rssi,
            entry->mac[0],entry->mac[1],entry->mac[2],
            entry->mac[3],entry->mac[4],entry->mac[5]);
    return 0;
}

/*****************************************************************************/

int list_read(entry_t* entry)
{
    if (List.counter == 0)
        return -1;
    memcpy(entry, &List.buffer[--List.counter], sizeof(entry_t));
    trace(TRACE_DEBUG, "List> read [%d] %d (%d/%d) %02x%02x%02x%02x%02x%02x\n",
            List.counter,
            entry->timestamp, entry->rssi, entry->count,
            entry->mac[0],entry->mac[1],entry->mac[2],
            entry->mac[3],entry->mac[4],entry->mac[5]);
    return 0;
}

/*****************************************************************************/

void list_clear(void)
{
    List.counter = 0;
    memset(List.buffer, 0, List.size * sizeof(entry_t));
}

/*****************************************************************************/
