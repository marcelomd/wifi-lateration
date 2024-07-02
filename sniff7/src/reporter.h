/*
 * reporter.h
 */

#ifndef __REPORTER_H
#define __REPORTER_H

/* Initializes reporter objects.
 * return:  0 on success. Error code on error.
 */
int reporter_init(void);

/* Run reporter thread.
 * return:  0 on success. Error code on error;
 *          contents of *thread are undefined.
 */
int reporter_start(void);

/* TODO: Closes reporter thread and frees resources.
 */
void reporter_stop(void);

#endif // __REPORTER_H

