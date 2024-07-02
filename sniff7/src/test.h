/*
 * test.h
 */

#ifndef __TEST_H
#define __TEST_H

#include "entry.h"

typedef enum {
    TEST_NONE = 0,  // No tests performed.
    TEST_FIXED,     // Tests using fixed table of devices.
} test_mode_t;

int test_init(void);

int test_get_entry(entry_t* entry);

#endif // __TEST_H
