/*
 * test.c
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>

#include "config.h"
#include "trace.h"
#include "entry.h"
#include "test.h"

/*****************************************************************************/

static int count = 0;

/*****************************************************************************/

int test_init(void)
{
    srand(1);
    count = 0;
    return 0;
}

/*****************************************************************************/

int test_get_entry(entry_t* entry)
{
    int t = time(NULL);

    entry->timestamp = t - (count % Config.report_interval);
    entry->count = 1;
    entry->rssi = 77;
    entry->mac[0] = 0xf7;
    entry->mac[1] = Config.mac[3];
    entry->mac[2] = Config.mac[4];
    entry->mac[3] = Config.mac[5];
    entry->mac[4] = (count >> 8) & 0xff;
    entry->mac[5] = (count >> 0) & 0xff;

    if (++count >= Config.buffer_size)
        count = 0;

    return 0;
}

/*****************************************************************************/
