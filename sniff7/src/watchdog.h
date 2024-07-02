/*
 * watchdog.h
 */

#ifndef __WATCHDOG_H
#define __WATCHDOG_H

/* Show some activity to watchdog.
 */
void watchdog_ping(void);

/* Starts watchdog thread.
 * Stops/restart application if reporter thread stops.
 * See watchdog.c for more details.
 */
int watchdog_start(void);

/* Watchdog cleanup.
 */
void watchdog_stop(void);

#endif // __WATCHDOG_H
